from django.shortcuts import render, redirect, get_object_or_404
from .forms import CreatePostForm, EditPostForm, PostImageForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Post, PostLike, PostImage, PostView
from django.http import Http404
from django.utils.text import slugify
import random
from django.http import JsonResponse
from datetime import timedelta
from django.utils.timezone import now
import readtime
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from apps.accounts.models import UserFollow
from apps.comments.models import Comment, CommentLike
from .helper_func import get_client_ip
from apps.notifications.models import NotificationService


@login_required
def create_post(request):
    
    if request.method == 'POST':
        form = CreatePostForm(data = request.POST)
        
        if form.is_valid():
            data = form.cleaned_data
            
            post_obj = Post.objects.create(
                title = data['title'],
                author = request.user,
                slug = slugify(data['title']) + "".join([random.choice("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz") for _ in range(5)])
            )
            messages.success(request, "Post created successfully.")
            return redirect("posts:edit_post", uuid = post_obj.id)
    
    else:
        form = CreatePostForm()
    
    ctx = {
        "title": "Create Post | Blogy",
        "form" : form,
    }
    return render(request, "posts/create_post.html", context= ctx)

@login_required
def edit_post(request, uuid):
    post_obj = get_object_or_404(Post.objects.filter(author = request.user), id = uuid, is_banned = False)
    old_title = post_obj.title
    
    if request.method == 'POST':
        form = EditPostForm(data = request.POST, files=request.FILES, instance= post_obj)
        
        if form.is_valid():
            data = form.cleaned_data

            if old_title != data['title']:
                post_obj.slug = slugify(data['title']) + "".join([random.choice("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz") for _ in range(5)])

            if data['content']:
                result = readtime.of_html(data['content'])
                post_obj.read_time = timedelta(seconds=result.seconds)
                post_obj.remove_unused_post_images()
            
            post_obj.updated_at = now()
            post_obj.content, post_obj.table_of_content = post_obj.generate_table_of_content_html()
            post_obj.save()
            post_obj.set_tags(data['tags'])
            
            messages.success(request, "Post saved successfully.")
            return redirect("posts:edit_post", uuid = post_obj.id)
    
    else:
        post_tags_str = ", ".join([str(tag.tag.name) for tag in post_obj.post_tags.all()])
        form = EditPostForm(instance= post_obj, initial= {"tags" : post_tags_str})
    
    ctx = {
        "title": f"Edit Post | {post_obj.title} | Blogy",
        "form" : form,
        "post_obj" : post_obj
    }
    return render(request, "posts/edit_post.html", context= ctx)

@login_required
def delete_post(request, uuid):
    post_obj = get_object_or_404(Post.objects.filter(author = request.user), id = uuid)
    
    if request.method == 'POST':
        post_obj.delete()
        messages.success(request, "Post deleted successfully.")
        return redirect("posts:my_posts")
    
    
    ctx = {
        "title": f"Delete Post | {post_obj.title} | Blogy",
        "post_obj" : post_obj
    }
    return render(request, "posts/delete_post.html", context= ctx)

@login_required
def my_posts(request):
    post_objs = Post.objects.filter(author = request.user).order_by("-created_at")
    
    paginator = Paginator(post_objs, 10)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)
    
    ctx = {
        "title": "My Posts | Blogy",
        "post_objs" : page_obj
    }
    return render(request, "posts/my_posts.html", context= ctx)

def post_detail(request, slug):
    post_obj = get_object_or_404(Post.objects.filter(is_banned = False), slug= slug)
    
    if post_obj.is_private and (not request.user.is_authenticated or post_obj.author != request.user):
        raise Http404()
    
    ip_address = get_client_ip(request)
    user_agent = request.META.get("HTTP_USER_AGENT", "")[:500]

    if request.user.is_authenticated:
        PostView.objects.get_or_create(
            post=post_obj,
            user=request.user,
            defaults={
                "ip_address": ip_address,
                "user_agent": user_agent,
            }
        )
    else:
        PostView.objects.get_or_create(
            post=post_obj,
            ip_address=ip_address,
            defaults={
                "user_agent": user_agent,
            }
        )
    
    is_following = request.user.is_authenticated and UserFollow.objects.filter(
        follower=request.user,
        following=post_obj.author
    ).exists()
    
    is_liked = request.user.is_authenticated and PostLike.objects.filter(
        post = post_obj,
        user = request.user
    ).exists()
    
    comments = Comment.objects.filter(
        post = post_obj,
        parent__isnull = True
    )
    
    if request.user.is_authenticated:
        user_comments = Comment.objects.filter(
            post = post_obj,
            user = request.user,
            parent__isnull = True
        )[:5]
        comments = comments.exclude(user = request.user)[:5]
        liked_comment_ids = set(
            CommentLike.objects.filter(
                user=request.user,
                comment__post_id = post_obj.id 
            ).values_list("comment_id", flat=True)
        )
    else:
        user_comments = Comment.objects.none()
        liked_comment_ids = set()
        comments = comments[:5]
    
    ctx = {
        "title" : f"{post_obj.title} | Blogy",
        "post_obj": post_obj,
        "is_following": is_following,
        "is_liked": is_liked,
        "user_comments": user_comments,
        "comments": comments,
        "liked_comment_ids": liked_comment_ids
    }
    
    return render(request, "posts/post_detail.html", ctx)

@login_required
def toggle_like(request, slug):
    if request.method == 'POST':
        post_obj = get_object_or_404(Post.objects.filter(is_banned = False, is_private = False), slug= slug)
        
        postLike_obj, created = PostLike.objects.get_or_create(
            user= request.user,
            post= post_obj,
        )
        
        if created:
            post_obj.likes_count += 1
            messages.success(request, "Post Liked.")
            NotificationService.create_post_like_notification(
                user=request.user,
                post_obj=post_obj
            )
        else:
            postLike_obj.delete()
            post_obj.likes_count -= 1
            messages.success(request, "Post Unliked.")
        post_obj.save()
        
        invalid_redirect_urls = [
            '/accounts/logout/',
            '/accounts/register/',
            '/accounts/login/'
        ]
        
        if request.POST.get("next") and request.POST.get("next") not in invalid_redirect_urls:
            return redirect(request.POST.get("next"))
        else:
            return redirect("posts:post_detail", slug)
    else:
        return redirect("posts:post_detail", slug)

@login_required
def liked_posts(request):
    post_objs = (
        Post.objects
        .filter(
            likes__user=request.user,
            is_private=False,
            is_banned=False,
        )
        .select_related("author")
        .distinct()
        .order_by("-likes__created_at")
    )
    
    paginator = Paginator(post_objs, 10)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)
    
    ctx = {
        "title": "Liked Posts | Blogy",
        "post_objs" : page_obj
    }
    return render(request, "posts/liked_posts.html", context= ctx)

@csrf_exempt
@login_required
def upload_image(request, slug):
    if request.method == "POST":
        post_obj = get_object_or_404(Post.objects.filter(is_banned = False, is_private = False, author= request.user), slug= slug)

        form = PostImageForm(data={"post": post_obj.id}, files={"image": request.FILES['file']})
        
        if form.is_valid():
            postImage_obj: PostImage = form.save()
            return JsonResponse({
                "location": postImage_obj.image.url
            },
            status= 201
            )
        else:
            return JsonResponse({'error': "Upload failed"}, status= 400)
    
    return JsonResponse({'error': "Wrong request"}, status= 403)
