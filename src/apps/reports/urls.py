from django.urls import path
from . import views

app_name = "reports"

urlpatterns = [
    path('user/<str:username>/', views.report_user, name='report_user'),
    path('post/<slug:slug>/', views.report_post, name='report_post'),
    path('comment/<uuid:pk>/', views.report_comment, name='report_comment'),
]
