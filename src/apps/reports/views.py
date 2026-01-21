from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.posts.models import Post
from apps.comments.models import Comment
from .models import PostReport, CommentReport, UserReport
from .forms import PostReportForm, CommentReportForm, UserReportForm
from django.contrib.auth import get_user_model

@login_required
def report_post(request, slug):
    post = get_object_or_404(Post, slug= slug)

    if post.author == request.user:
        messages.warning(request, "You cannot report your own post.")
        return redirect("posts:post_detail", slug=post.slug)

    if PostReport.objects.filter(
        reported_post=post,
        reported_by=request.user
    ).exists():
        messages.warning(request, "You have already reported this post.")
        return redirect("posts:post_detail", slug=post.slug)

    if request.method == "POST":
        data = {
            "reported_by": request.user,
            "reported_post": post,
            "subject": request.POST.get("subject"),
            "description": request.POST.get("description"),
        }
        form = PostReportForm(data= data)
        if form.is_valid():
            form.save()
            messages.success(request, "Report submitted successfully.")
            return redirect("posts:post_detail", slug=post.slug)
    else:
        form = PostReportForm()
    
    ctx = {
        "title": f"Report Post | {post.title} | Blogy",
        "post": post,
        "form": form
    }
    
    return render(request, "reports/report_post.html", ctx)

@login_required
def report_comment(request, pk):
    comment = get_object_or_404(Comment, pk= pk)

    if comment.user == request.user:
        messages.warning(request, "You cannot report your own comment.")
        invalid_redirect_urls = [
            '/accounts/logout/',
            '/accounts/register/',
            '/accounts/login/'
        ]
        if request.GET.get("next") and request.GET.get("next") not in invalid_redirect_urls:
            return redirect(request.GET.get("next"))
        else:
            return redirect("posts:post_detail", comment.post.slug)

    if CommentReport.objects.filter(
        reported_comment=comment,
        reported_by=request.user
    ).exists():
        messages.warning(request, "You have already reported this comment.")
        invalid_redirect_urls = [
            '/accounts/logout/',
            '/accounts/register/',
            '/accounts/login/'
        ]
        if request.GET.get("next") and request.GET.get("next") not in invalid_redirect_urls:
            return redirect(request.GET.get("next"))
        else:
            return redirect("posts:post_detail", comment.post.slug)

    if request.method == "POST":
        data = {
            "reported_by": request.user,
            "reported_comment": comment,
            "subject": request.POST.get("subject"),
            "description": request.POST.get("description"),
        }
        form = CommentReportForm(data= data)
        if form.is_valid():
            form.save()
            messages.success(request, "Report submitted successfully.")
            invalid_redirect_urls = [
                '/accounts/logout/',
                '/accounts/register/',
                '/accounts/login/'
            ]
            if request.GET.get("next") and request.GET.get("next") not in invalid_redirect_urls:
                return redirect(request.GET.get("next"))
            else:
                return redirect("posts:post_detail", comment.post.slug)
    else:
        form = CommentReportForm()
    
    ctx = {
        "title": f"Report Comment | {comment.pk} | Blogy",
        "comment": comment,
        "form": form
    }
    
    return render(request, "reports/report_comment.html", ctx)

@login_required
def report_user(request, username):
    user_obj = get_object_or_404(get_user_model(), username= username)

    if user_obj == request.user:
        messages.warning(request, "You cannot report your own account.")
        return redirect("acc_public_urls:author_profile", username=user_obj.username)

    if UserReport.objects.filter(
        reported_to=user_obj,
        reported_by=request.user
    ).exists():
        messages.warning(request, "You have already reported this account.")
        return redirect("acc_public_urls:author_profile", username=user_obj.username)

    if request.method == "POST":
        data = {
            "reported_by": request.user,
            "reported_to": user_obj,
            "subject": request.POST.get("subject"),
            "description": request.POST.get("description"),
        }
        form = UserReportForm(data= data)
        if form.is_valid():
            form.save()
            messages.success(request, "Report submitted successfully.")
            return redirect("acc_public_urls:author_profile", username=user_obj.username)
    else:
        form = UserReportForm()
    
    ctx = {
        "title": f"Report User | {user_obj.username} | Blogy",
        "user_obj": user_obj,
        "form": form
    }
    
    return render(request, "reports/report_user.html", ctx)
