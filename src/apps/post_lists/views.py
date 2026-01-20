from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count
from .models import PostList, PostListItem, PostListLike
from .forms import PostListForm
from django.contrib import messages
from apps.posts.models import Post
from apps.notifications.models import NotificationService
from django.utils.timezone import now
from django.views.decorators.http import require_POST


@login_required
def my_post_lists(request):

    if request.method == "POST":
        form = PostListForm(data= request.POST)
        if form.is_valid():
            post_list = form.save(commit=False)
            post_list.user = request.user
            post_list.save()
            return redirect("post_lists:my_post_lists")
    else:
        form = PostListForm()

    qs = (
        PostList.objects
        .filter(user=request.user)
        .annotate(
            likes_count=Count("list_likes", distinct=True),
            posts_count=Count("post_list_items", distinct=True),
        )
        .order_by("-created_at")
    )

    paginator = Paginator(qs, 5)
    page_number = request.GET.get("page")
    post_lists = paginator.get_page(page_number)

    ctx = {
        "title" : "My Post Lists | Blogy",
        "post_lists": post_lists,
        "form": form,
    }
    
    return render(request, "post_lists/my_post_lists.html", ctx)

@login_required
def delete_post_list(request, pk):
    post_list = get_object_or_404(
        PostList,
        id=pk,
        user=request.user
    )

    post_list.delete()
    messages.success(request, "Post List Deleted successfully.")
    return redirect("post_lists:my_post_lists")

@login_required
def edit_post_list(request, pk):
    post_list = get_object_or_404(
        PostList,
        pk=pk,
        user=request.user
    )

    items_qs = (
    PostListItem.objects
    .filter(post_list=post_list)
    .select_related("post", "post__author")
    .order_by("order", "created_at")
)

    items = list(items_qs)

    # attach prev / next ids
    for index, item in enumerate(items):
        item.prev_id = items[index - 1].id if index > 0 else None
        item.next_id = items[index + 1].id if index < len(items) - 1 else None

    if request.method == "POST":
        form = PostListForm(request.POST, instance=post_list)
        if form.is_valid():
            postList_obj = form.save(commit=False)
            postList_obj.updated_at = now()
            postList_obj.save()
            messages.success(request, "Post List Updated successfully.")
            return redirect("post_lists:edit_post_list", pk=post_list.pk)
    else:
        form = PostListForm(instance=post_list)
    
    ctx = {
        "post_list": post_list,
        "items": items,
        "form": form,
    }
    
    return render(request, "post_lists/edit_post_list.html", ctx)

@login_required
def post_list_item_reorder(request, upper, lower):
    post_list_item_upper = get_object_or_404(PostListItem, pk = upper, post_list__user = request.user)
    post_list_item_lower = get_object_or_404(PostListItem, pk = lower, post_list__user = request.user)
    if request.method == 'POST' and post_list_item_lower.post_list == post_list_item_upper.post_list:
        
        temp_order = post_list_item_upper.order
        post_list_item_upper.order = post_list_item_lower.order
        post_list_item_lower.order = temp_order
        
        post_list_item_upper.save()
        post_list_item_lower.save()
        
        messages.success(request, "Reodered Successfully.")
        return redirect("post_lists:edit_post_list", pk = post_list_item_upper.post_list.pk)
    else:
        invalid_redirect_urls = [
            '/accounts/logout/',
            '/accounts/register/',
            '/accounts/login/'
        ]
        
        if request.POST.get("next") and request.POST.get("next") not in invalid_redirect_urls:
            return redirect(request.POST.get("next"))
        else:
            return redirect("post_lists:edit_post_list", pk = post_list_item_upper.post_list.pk)

@login_required
def delete_post_list_item(request, pk):
    post_list_item_obj = get_object_or_404(
        PostListItem,
        id=pk,
        post_list__user=request.user
    )
    post_list_id = post_list_item_obj.post_list.pk
    post_list_item_obj.delete()
    messages.success(request, "Post List Item removed.")
    return redirect("post_lists:edit_post_list", pk = post_list_id)

@login_required
def save_post(request, post_pk):
    post_obj = get_object_or_404(Post, pk= post_pk)
    
    lists_qs = (
        PostList.objects
        .filter(user=request.user)
        .order_by("-created_at")
    )
    
    paginator = Paginator(lists_qs, 10)
    page_number = request.GET.get("page")
    post_lists = paginator.get_page(page_number)
    
    ctx = {
        "title" : "Save to Post Lists | Blogy",
        "post": post_obj,
        "post_lists": post_lists,
    }
    
    return render(request, "post_lists/save_post.html", ctx )

@login_required
def add_post_to_list(request, post_pk, list_id):
    post = get_object_or_404(Post, pk=post_pk)
    post_list = get_object_or_404(PostList, pk=list_id, user=request.user)

    postListItem_obj, created = PostListItem.objects.get_or_create(
        post_list=post_list,
        post=post,
        defaults={"order": post_list.post_list_items.count() + 1}
    )

    if created:
        messages.success(request, "Post added to list.")
    else:
        messages.warning(request, "Post already in the list.")
    
    invalid_redirect_urls = [
        '/accounts/logout/',
        '/accounts/register/',
        '/accounts/login/'
    ]
    
    if request.GET.get("next") and request.GET.get("next") not in invalid_redirect_urls:
        return redirect(request.GET.get("next"))
    else:
        return redirect("post_lists:save_post", post_pk=post.id)

def post_list_detail(request, pk):
    post_list = get_object_or_404(
        PostList.objects.select_related("user"),
        pk=pk
    )

    items_qs = (
        PostListItem.objects
        .filter(post_list=post_list)
        .select_related("post", "post__author")
        .order_by("order")
    )

    paginator = Paginator(items_qs, 10)
    page_number = request.GET.get("page")
    items = paginator.get_page(page_number)

    # post list like info
    is_liked = False
    if request.user.is_authenticated:
        is_liked = PostListLike.objects.filter(
            post_list=post_list,
            user=request.user
        ).exists()

    ctx = {
        "title": f"{post_list.title} | Post List | Blogy",
        "post_list": post_list,
        "items": items,
        "is_liked": is_liked,
    }
    
    return render(request, "post_lists/post_list_detail.html", ctx)

@login_required
@require_POST
def toggle_post_list_like(request, pk):
    post_list = get_object_or_404(PostList, pk=pk)

    like, created = PostListLike.objects.get_or_create(
        post_list=post_list,
        user=request.user
    )

    if not created:
        messages.success(request, "Post List Unliked.")
        like.delete()
        post_list.likes -= 1
    else:
        messages.success(request, "Post List Liked.")
        post_list.likes += 1
        NotificationService.create_post_list_like_notification(
                user=request.user,
                post_list=post_list
        )
        
    post_list.save()

    invalid_redirect_urls = [
        '/accounts/logout/',
        '/accounts/register/',
        '/accounts/login/'
    ]
    
    if request.POST.get("next") and request.POST.get("next") not in invalid_redirect_urls:
        return redirect(request.POST.get("next"))
    else:
        return redirect("post_lists:post_list_detail", pk=pk)
