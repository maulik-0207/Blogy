from uuid import uuid4
from django.contrib import messages
from .tasks import send_reset_password_link
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model, authenticate, login, logout
from .forms import RegisterForm, ProfileForm, ResetPasswordForm, ChangePasswordForm


def login_view(request):
    if request.user.is_authenticated:
        messages.warning(request, "Already Logged in.")
        return redirect("main:home")
    
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        user_obj = authenticate(request, username = username, password = password)

        if user_obj and user_obj.is_verified == True and user_obj.is_banned == False:
            login(request, user_obj)
            messages.success(request, "Logged in successfully.")
            invalid_redirect_urls = [
                '/accounts/logout/',
                '/accounts/register/',
                '/accounts/login/',
            ]
            if request.GET.get("next") and not request.GET.get("next") in invalid_redirect_urls:
                return redirect(request.GET.get("next"))
            else:
                return redirect("main:home")
        elif user_obj and user_obj.is_verified == False:
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
            messages.success(request, f"We have sent a verification link to your email.")
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
    except:
        messages.info(request, "Invalid Verification Link.")
        return redirect("main:home")
    
    if not user_obj:
        messages.info(request, "Invalid Verification Link.")
        return redirect("main:home")
    
    if request.method == 'POST':
        user_obj.is_verified = True
        user_obj.uuid = None
        user_obj.save()
        messages.success(request, "Account verified successfully.")
        return redirect("accounts:login")
    
    ctx = {
        "title": "Verify Account | Blogy",
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
        except:
            messages.info(request, "No such account with this email id.")
            return redirect("accounts:forgot_password")
        
        user_obj.uuid = uuid4()
        user_obj.save()
        send_reset_password_link.delay(request.scheme, request.get_host(), user_obj.username, user_obj.email, user_obj.uuid)
        messages.success(request, "We have sent a reset password link to your mail.")
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
    except:
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
            valid_user = authenticate(request, username = request.user.username, password =current_password )
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
