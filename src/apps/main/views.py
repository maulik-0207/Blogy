from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.contrib.auth import get_user_model
from apps.posts.models import Post
from apps.post_lists.models import PostList
import random

def home(request):
    
    user = request.user

    followed_users = []
    if user.is_authenticated:
        followed_users = [obj.pk for obj in user.followings.all()]

    posts_qs = (
        Post.objects
        .select_related("author")
        .filter(Q(author_id__in=followed_users) | Q (author_id__isnull=False), is_private=False, is_banned=False)
        .exclude(author_id = user.pk if user.is_authenticated else None)
        .order_by("-created_at")[:70]
    )

    post_lists_qs = (
        PostList.objects
        .select_related("user")
        .annotate(
            posts_count=Count("post_list_items", distinct=True),
        )
        .exclude(user_id = user.pk)
        .order_by("-created_at")[:30]
    )

    feed_items = []

    for post in posts_qs:
        post.feed_type = "post"
        feed_items.append(post)

    for pl in post_lists_qs:
        pl.feed_type = "post_list"
        feed_items.append(pl)

    random.shuffle(feed_items)

    paginator = Paginator(feed_items, 10)
    page_number = request.GET.get("page")
    feed = paginator.get_page(page_number)
    
    trending_authors = (
        get_user_model().objects
        .exclude(pk= user.pk if user.is_authenticated else None)
        .order_by("-followers_count")[:8]
    )
    
    ctx = {
        "title": "Home | Blogy",
        "feed": feed,
        "trending_authors": trending_authors,
    }
    
    return render(request, "index.html", context= ctx)

def search(request):
    query = request.GET.get("q", "").strip()
    content_type = request.GET.get("type", "all")  # all | posts | lists | authors
    page_number = request.GET.get("page")

    results = []

    # POSTS
    if content_type in ("all", "posts") and query:
        posts = (
            Post.objects
            .filter(
                title__icontains=query,
                is_private=False,
                is_banned=False,
            )
            .select_related("author")
            .order_by("-created_at")[:70]
        )

        for post in posts:
            post.feed_type = "post"
            results.append(post)

    # POST LISTS
    if content_type in ("all", "lists") and query:
        post_lists = (
            PostList.objects
            .filter(
                title__icontains=query
            )
            .select_related("user")
            .annotate(
                posts_count=Count("post_list_items", distinct=True),
            )
            .order_by("-created_at")[:30]
        )

        for pl in post_lists:
            pl.feed_type = "post_list"
            results.append(pl)

    # AUTHORS
    if content_type in ("all", "authors") and query:
        authors = (
            get_user_model()
            .objects
            .filter(
                Q(username__icontains=query) |
                Q(name__icontains=query)
            )
            .order_by("-followers_count")[:30]
        )

        for author in authors:
            author.feed_type = "author"
            results.append(author)
    
    paginator = Paginator(results, 10)
    page_obj = paginator.get_page(page_number)

    ctx = {
        "query": query,
        "content_type": content_type,
        "results": page_obj,
    }
    
    return render(request, "search.html", ctx)


def error_400(request, exception):
    return render(request, "errors/400.html", status=400)


def error_403(request, exception):
    return render(request, "errors/403.html", status=403)


def error_404(request, exception):
    return render(request, "errors/404.html", status=404)


def error_500(request):
    return render(request, "errors/500.html", status=500)
