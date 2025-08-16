from django.urls import path
from .views import *

app_name = "accounts"

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register, name='register'),
    path('verify-email/<uuid>/', verify_email, name='verify_email'),
    path('edit-profile/', edit_profile, name='edit_profile'),
    path('forgot-password/', forgot_password, name='forgot_password'),
    path('reset-password/<uuid>/', reset_password, name='reset_password'),
    path('change-password/', change_password, name='change_password'),
]
