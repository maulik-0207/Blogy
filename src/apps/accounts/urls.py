from django.urls import path
from .views import *

app_name = "accounts"

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register, name='register'),
    path('verify-email/<uuid>/', verify_email, name='verify_email'),
]
