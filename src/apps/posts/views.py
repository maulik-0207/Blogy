from django.shortcuts import render, redirect, get_object_or_404
from .forms import CreatePostForm, EditPostForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Post, Tag, PostTag
from django.utils.text import slugify
import random
import copy

@login_required
def create_post(request):
    
    if request.method == 'POST':
        form = CreatePostForm(data = request.POST)
        
        if form.is_valid():
            data = form.cleaned_data
            
            post_obj = Post.objects.create(
                title = data['title'],
                author = request.user,
                slug = slugify(data['title']) + "-" + "".join([random.choice("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz") for _ in range(5)])
            )
            post_obj.save()
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
    old_post_obj = copy.deepcopy(post_obj)
    post_tags = [str(tag.tag.name) for tag in post_obj.post_tags.all()]
    
    if request.method == 'POST':
        form = EditPostForm(data = request.POST, files=request.FILES, instance= post_obj)
        
        if form.is_valid():
            data = form.cleaned_data

            
            if old_post_obj.title != data['title']:
                post_obj.slug = slugify(data['title']) + "-" + "".join([random.choice("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz") for _ in range(5)])

            post_obj.save()
            
            tags_input = [tag.lower().strip() for tag in str(data['tags_input']).split(",")]
            for tag in tags_input[:5]:
                if not tag in post_tags and tag != "":
                    tag_obj = Tag.objects.get_or_create(name = tag)[0]
                    postTag_obj = PostTag.objects.create(post = post_obj, tag = tag_obj)
            
            for tag in post_tags:
                if not tag in tags_input:
                    postTag_obj = PostTag.objects.get(post = post_obj, tag__name = tag)
                    postTag_obj.delete()
            
            messages.success(request, "Post saved successfully.")
            return redirect("posts:edit_post", uuid = post_obj.id)
    
    else:
        post_tags_str = ", ".join(post_tags)
        form = EditPostForm(instance= post_obj, initial= {"tags_input" : post_tags_str})
    
    ctx = {
        "title": f"Edit Post | {post_obj.title} | Blogy",
        "form" : form,
        "post_obj" : post_obj
    }
    return render(request, "posts/edit_post.html", context= ctx)

@login_required
def delete_post(request, uuid):
    post_obj = get_object_or_404(Post.objects.filter(author = request.user), id = uuid, is_banned = False)
    
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
    post_objs = Post.objects.filter(author = request.user, is_banned = False)
    
    
    ctx = {
        "title": f"My Posts | Blogy",
        "post_objs" : post_objs
    }
    return render(request, "posts/my_posts.html", context= ctx)