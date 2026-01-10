from django.urls import path
from . import views

app_name = "notifications"

urlpatterns = [
    path("", views.notification_list, name="notification_list"),
    path("delete/<uuid:pk>/", views.notification_delete, name="notification_delete"),
]
