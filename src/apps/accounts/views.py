from .forms import RegisterForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model, authenticate, login, logout


def login_view(request):
    if request.user.is_authenticated:
        messages.warning(request, "Already Logged in.")
        return redirect("main:home")
    
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        user_obj = authenticate(request,username = username, password = password)

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
    messages.success(request,"Logged out successfully.")
    return redirect("accounts:login")

def register(request):
    if request.user.is_authenticated:
        messages.warning(request, "Already Logged in.")
        return redirect("main:home")
    
    if request.method == 'POST':
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            form.save(request= request)
            messages.success(request,f"We have sent a verification link to your email.")
            return redirect("accounts:login")
    else:
        form = RegisterForm()
    
    ctx = {
        "title" : "Register | Blogy",
        "form" : form,
    }
    return render(request, "accounts/register.html", ctx)

def verify_email(request, uuid):
    
    messages.info(request, f"Visited verify email: {uuid}")
    return redirect("accounts:login")