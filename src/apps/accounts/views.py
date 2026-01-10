from uuid import uuid4
from django.contrib import messages
from .tasks import send_reset_password_link
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model, authenticate, login, logout
from .forms import RegisterForm, ProfileForm, ResetPasswordForm, ChangePasswordForm
from django.core.paginator import Paginator
from apps.posts.models import Post
from .models import UserFollow
from apps.notifications.models import NotificationService


def login_view(request):
    if request.user.is_authenticated:
        messages.warning(request, "Already Logged in.")
        return redirect("main:home")

    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")

        user_obj = authenticate(request, username = username, password = password)

        if user_obj and user_obj.is_verified and not user_obj.is_banned:
            login(request, user_obj)
            messages.success(request, "Logged in successfully.")
            invalid_redirect_urls = [
                '/accounts/logout/',
                '/accounts/register/',
                '/accounts/login/',
            ]
            if request.POST.get("next") and request.POST.get("next") not in invalid_redirect_urls:
                return redirect(request.POST.get("next"))
            else:
                return redirect("main:home")
        elif user_obj and not user_obj.is_verified:
            messages.warning(request, 'Account is not verified.')
            return redirect("accounts:login")
        else:
            messages.warning(request, "Invalid Credentials.")
            return redirect("accounts:login")
            
    ctx = {
        "title": "Login | Blogy",
    }
    return render(request, "accounts/login.html", context= ctx)

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect("accounts:login")

def register(request):
    if request.user.is_authenticated:
        messages.warning(request, "Already Logged in.")
        return redirect("main:home")
    
    if request.method == 'POST':
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            form.save(request= request)
            messages.success(request, "We have sent a verification link to your email.")
            return redirect("accounts:login")
    else:
        form = RegisterForm()
    
    ctx = {
        "title" : "Register | Blogy",
        "form" : form,
    }
    return render(request, "accounts/register.html", ctx)

def verify_email(request, uuid):
    if request.user.is_authenticated:
        messages.warning(request, "Already Logged in.")
        return redirect("main:home")
    
    try:
        user_obj = get_user_model().objects.get(uuid = uuid, is_verified = False)
    except (get_user_model().DoesNotExist, ValueError):
        messages.info(request, "Invalid Verification Link.")
        return redirect("main:home")
    
    if request.method == 'POST':
        user_obj.is_verified = True
        user_obj.uuid = None
        user_obj.save()
        messages.success(request, "Email verified successfully.")
        return redirect("accounts:login")
    
    ctx = {
        "title": "Verify Your Email | Blogy",
        "user" : user_obj,
    }
    
    return render(request, 'accounts/verification.html', context= ctx)

@login_required
def edit_profile(request): 
    
    if request.method == "POST":
        form = ProfileForm(instance= request.user, data= request.POST, files= request.FILES)
        
        if form.is_valid():
            form.save()
            messages.success(request, "Profile Saved Successfully.")
            return redirect("accounts:edit_profile")
    else:
        form = ProfileForm(instance= request.user)
        
    ctx = {
        "title" : "Edit Profile | Blogy",
        "form" : form
    }
    
    return render(request, "accounts/edit_profile.html", context= ctx)

def forgot_password(request):
    if request.user.is_authenticated:
        messages.warning(request, "Already Logged in.")
        return redirect("main:home")
    
    if request.method == 'POST':
        email = request.POST.get("email")
        
        try:
            user_obj = get_user_model().objects.get(email = email, is_active = True, is_verified = True)
        except (get_user_model().DoesNotExist, ValueError):
            messages.info(request, "No such account with this email id.")
            return redirect("accounts:forgot_password")
        
        user_obj.uuid = uuid4()
        user_obj.save()
        send_reset_password_link.delay(request.scheme, request.get_host(), user_obj.username, user_obj.email, user_obj.uuid)
        messages.success(request, "We have sent a reset password link to your email.")
        return redirect("accounts:login")

    ctx = {
        "title" : "Forgot Password | Blogy",
    }
    return render(request, "accounts/forgot_password.html", context=ctx)

def reset_password(request, uuid):
    if request.user.is_authenticated:
        messages.warning(request, "Already Logged in.")
        return redirect("main:home")
    
    try:
        user_obj = get_user_model().objects.get(uuid = uuid, is_active = True, is_verified = True)
    except (get_user_model().DoesNotExist, ValueError):
        messages.info(request, "Invalid Link.")
        return redirect("accounts:forgot_password")
    
    if request.method == 'POST':
    
        form = ResetPasswordForm(data=request.POST)
        if form.is_valid():
            user_obj.uuid = None
            user_obj.set_password(form.cleaned_data["password"])
            user_obj.save()
            messages.success(request, "Password changed successfully.")
            return redirect("accounts:login")
    else:
        form = ResetPasswordForm()
    
    ctx = {
        "title" : "Reset Password | Blogy",
        "form" : form,
    }
    return render(request, "accounts/reset_password.html", context=ctx)

@login_required
def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(data=request.POST)
        if form.is_valid():
            current_password = form.cleaned_data["current_password"]
            valid_user = authenticate(request, username= request.user.username, password= current_password )
            if not valid_user:
                form.add_error("current_password","Current Password is incorrect.")
            else:
                valid_user.set_password(form.cleaned_data['new_password'])
                valid_user.save()
                login(request, valid_user)
                messages.success(request, "Password Changed successfully.")
                return redirect("accounts:change_password")
    else:
        form = ChangePasswordForm()
    
    ctx = {
        "title" : "Change Password | Blogy",
        "form" : form,
    }
    return render(request, "accounts/change_password.html", context=ctx)

def author_profile(request, username):
    author = get_object_or_404(
        get_user_model(),
        username=username,
        is_active=True,
        is_verified = True,
        is_banned = False
    )

    is_following = request.user.is_authenticated and UserFollow.objects.filter(
        follower=request.user,
        following=author
    ).exists()

    post_objs = (
        Post.objects
        .filter(author=author, is_banned=False)
        .select_related("author")
        .prefetch_related("post_tags__tag")
        .order_by("-created_at")
    )

    if request.user != author:
        post_objs = post_objs.filter(is_private=False)

    filter_type = request.GET.get("filter", "all")

    if filter_type == "public":
        post_objs = post_objs.filter(is_private=False)

    elif filter_type == "popular":
        post_objs = post_objs.order_by("-likes_count")

    paginator = Paginator(post_objs, 10) 
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)

    ctx = {
        "title": f"{author.username} | Blogy",
        "author": author,
        "page_obj": page_obj,
        "filter": filter_type,
        "is_following": is_following,
    }

    return render(request, "accounts/author_profile.html", ctx)

@login_required
def toggle_follow(request, username):
    
    if request.method == 'POST':
        author = get_object_or_404(
            get_user_model(),
            username=username,
            is_active=True,
            is_verified = True,
            is_banned = False
        )

        userFollow_obj, created = UserFollow.objects.get_or_create(
            follower= request.user,
            following = author,
        )
        
        if created:
            request.user.followings_count += 1
            author.followers_count += 1
            messages.success(request, "Author Followed.")
            is_follow_back = UserFollow.objects.filter(
                follower=author,
                following=request.user
            ).exists()

            if is_follow_back:
                NotificationService.create_follow_back_notification(
                    follower=request.user,
                    following=author
                )
            else:
                NotificationService.create_follow_notification(
                    follower=request.user,
                    following=author
                )
        else:
            userFollow_obj.delete()
            request.user.followings_count -= 1
            author.followers_count -= 1
            messages.success(request, "Author Unfollowed.")
        
        request.user.save()
        author.save()
            
        invalid_redirect_urls = [
            '/accounts/logout/',
            '/accounts/register/',
            '/accounts/login/'
        ]
        
        if request.POST.get("next") and request.POST.get("next") not in invalid_redirect_urls:
            return redirect(request.POST.get("next"))
        else:
            return redirect("acc_public_urls:author_profile", author.username)
    else:
        return redirect("acc_public_urls:author_profile", username)

@login_required
def followings(request):
    userFollow_objs = UserFollow.objects.select_related("following").filter(
        follower=request.user
    ).order_by("-created_at")

    paginator = Paginator(userFollow_objs, 10)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)

    ctx = {
        "title": "Followings | Blogy",
        "page_obj": page_obj
    }
    
    return render(request, "accounts/followings.html", ctx)

@login_required
def followers(request):
    userFollow_objs = UserFollow.objects.select_related("follower").filter(
        following=request.user
    ).order_by("-created_at")


    paginator = Paginator(userFollow_objs, 10)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)
    
    followers_ids = [obj.follower_id for obj in page_obj]
    
    following_ids = set(
        UserFollow.objects.filter(
            follower=request.user,
            following_id__in = followers_ids
        ).values_list("following_id", flat=True)
    )
    
    ctx = {
        "title": "Followers | Blogy",
        "page_obj": page_obj,
        "following_ids": following_ids,
    }
    
    return render(request, "accounts/followers.html", ctx)
