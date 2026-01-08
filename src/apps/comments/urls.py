from django.urls import path
from . import views

app_name = "comments"

urlpatterns = [
    path('create/<slug:slug>/', views.create_comment, name='create_comment'),
    path('my/<slug:slug>/', views.my_comments, name='my_comments'),
    path('all/<slug:slug>/', views.all_comments, name='all_comments'),
    path('toggle-like/<uuid:comment_id>/', views.toggle_like, name='toggle_like'),
    path('delete/<uuid:comment_id>/', views.delete_comment, name='delete_comment'),
]
