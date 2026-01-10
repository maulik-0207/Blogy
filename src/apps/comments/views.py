from django.shortcuts import render, get_object_or_404, redirect
from apps.posts.models import Post
from .forms import CommentForm
from .models import Comment, CommentLike
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from apps.notifications.models import NotificationService


@login_required
def create_comment(request, slug):
    
    if request.method == 'POST':
        post_obj = get_object_or_404(Post.objects.filter(is_banned = False, is_private = False), slug= slug)
         
        data = {
            'user': request.user.id, 
            'post': post_obj.id, 
            'content': request.POST.get("content"),
            'parent': request.POST.get("parent", None),
        }
        form = CommentForm(data= data)
        if form.is_valid():
            comment_obj = Comment.objects.create(
                user= request.user,
                post = post_obj,
                content = form.cleaned_data['content'],
                parent = form.cleaned_data['parent']
            )
            post_obj.comments_count += 1
            post_obj.save()
            if data['parent']:
                messages.success(request, "Replied successfully.")
            else:
                messages.success(request, "Commented successfully.")
            NotificationService.create_comment_notification(
                request.user, 
                comment_obj, 
                post_obj
            )
        else:
            messages.warning(request, form.errors['content'][0].replace("This field", ("Reply" if data['parent'] else "Comment")))

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
        messages.warning(request, "Wrong method.")
        return redirect("posts:post_detail", slug)

@login_required
def toggle_like(request, comment_id):
    comment_obj = get_object_or_404(Comment, pk= comment_id)
    if request.method == 'POST':
        
        commentLike_obj, created = CommentLike.objects.get_or_create(
            user= request.user,
            comment= comment_obj,
        )
        
        if created:
            comment_obj.likes += 1
            messages.success(request, f"{"Reply" if comment_obj.parent else "Comment" } Liked.")
            NotificationService.create_comment_like_notification(
                user=request.user,
                comment_obj=comment_obj
            )
        else:
            commentLike_obj.delete()
            comment_obj.likes -= 1
            messages.success(request, f"{"Reply" if comment_obj.parent else "Comment" } Unliked.")
        comment_obj.save()
        
        invalid_redirect_urls = [
            '/accounts/logout/',
            '/accounts/register/',
            '/accounts/login/'
        ]
        
        if request.POST.get("next") and request.POST.get("next") not in invalid_redirect_urls:
            return redirect(request.POST.get("next"))
        else:
            return redirect("posts:post_detail", comment_obj.post.slug)
    else:
        return redirect("posts:post_detail", comment_obj.post.slug)

@login_required
def delete_comment(request, comment_id):
    comment_obj = get_object_or_404(Comment, pk= comment_id)
    if request.method == 'POST':
        post_obj = comment_obj.post
        messages.success(request, f"{"Reply" if comment_obj.parent else "Comment" } Deleted.")
        deleted_count, deleted_map = comment_obj.delete()
        post_obj.comments_count -= deleted_count
        post_obj.save()
        invalid_redirect_urls = [
            '/accounts/logout/',
            '/accounts/register/',
            '/accounts/login/'
        ]
        
        if request.POST.get("next") and request.POST.get("next") not in invalid_redirect_urls:
            return redirect(request.POST.get("next"))
        else:
            return redirect("posts:post_detail", post_obj.slug)
    else:
        messages.warning(request, "Invalid method.")
        return redirect("posts:post_detail", comment_obj.post.slug)

@login_required
def my_comments(request, slug):
    post_obj = get_object_or_404(Post.objects.filter(is_banned = False, is_private = False), slug= slug)
    
    user_comments = Comment.objects.filter(
        post = post_obj,
        user = request.user,
        parent__isnull = True
    )
    paginator = Paginator(user_comments, 10)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)
    
    liked_comment_ids = set(
        CommentLike.objects.filter(
            user=request.user,
            comment_id__in = [cmt.id for cmt in page_obj] 
        ).values_list("comment_id", flat=True)
    )
    
    ctx = {
        "title" : "My Comments | Blogy",
        "post_obj": post_obj,
        "user_comments": page_obj,
        "liked_comment_ids": liked_comment_ids
    }
    
    return render(request, "comments/my_comments.html", ctx)

def all_comments(request, slug):
    post_obj = get_object_or_404(Post.objects.filter(is_banned = False, is_private = False), slug= slug)
    
    all_comments = Comment.objects.filter(
        post = post_obj,
        parent__isnull = True
    )
    paginator = Paginator(all_comments, 10)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)
    
    if request.user.is_authenticated:
        liked_comment_ids = set(
            CommentLike.objects.filter(
                user=request.user,
                comment_id__in = [cmt.id for cmt in page_obj] 
            ).values_list("comment_id", flat=True)
        )
    else:
        liked_comment_ids = set()
    
    ctx = {
        "title" : "Comments | Blogy",
        "post_obj": post_obj,
        "all_comments": page_obj,
        "liked_comment_ids": liked_comment_ids
    }
    
    return render(request, "comments/all_comments.html", ctx)
