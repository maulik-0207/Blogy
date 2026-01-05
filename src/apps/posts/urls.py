from django.urls import path
from . import views

app_name = "posts"

urlpatterns = [
    path('', views.my_posts, name='my_posts'),
    path('<slug:slug>', views.post_detail, name='post_detail'),
    path('create/', views.create_post, name='create_post'),
    path('edit/<uuid:uuid>/', views.edit_post, name='edit_post'),
    path('delete/<uuid:uuid>/', views.delete_post, name='delete_post'),
]
