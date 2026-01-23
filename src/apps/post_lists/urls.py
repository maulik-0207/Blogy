from django.urls import path
from . import views

app_name = "post_lists"

urlpatterns = [
    path('', views.my_post_lists, name='my_post_lists'),
    path('liked/', views.my_liked_post_lists, name='my_liked_post_lists'),
    path("<uuid:pk>/", views.post_list_detail, name="post_list_detail"),
    path("<uuid:pk>/like/", views.toggle_post_list_like, name="toggle_post_list_like"),
    path('save-post/<uuid:post_pk>/', views.save_post, name='save_post'),
    path('delete/<uuid:pk>/', views.delete_post_list, name='delete_post_list'),
    path('edit/<uuid:pk>/', views.edit_post_list, name='edit_post_list'),
    path('items/<uuid:post_pk>/<uuid:list_id>/', views.add_post_to_list, name='add_post_to_list'),
    path('items/delete/<uuid:pk>/', views.delete_post_list_item, name='delete_post_list_item'),
    path('items/reorder/<uuid:upper>/<uuid:lower>/', views.post_list_item_reorder, name='post_list_item_reorder'),
]
