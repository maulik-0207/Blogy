from django.shortcuts import render, redirect, get_object_or_404
from .forms import CreatePostForm, EditPostForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Post
from django.http import Http404
from django.utils.text import slugify
import random
from datetime import timedelta
from django.utils.timezone import now
import readtime
from apps.accounts.models import UserFollow

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
    
    ctx = {
        "title": "My Posts | Blogy",
        "post_objs" : post_objs
    }
    return render(request, "posts/my_posts.html", context= ctx)

def post_detail(request, slug):
    post_obj = get_object_or_404(Post.objects.filter(is_banned = False), slug= slug)
    
    if post_obj.is_private and (not request.user.is_authenticated or post_obj.author != request.user):
        raise Http404()
    
    is_following = request.user.is_authenticated and UserFollow.objects.filter(
        follower=request.user,
        following=post_obj.author
    ).exists()
    
    ctx = {
        "title" : f"{post_obj.title} | Blogy",
        "post_obj": post_obj,
        "is_following": is_following
    }
    
    return render(request, "posts/post_detail.html", ctx)
