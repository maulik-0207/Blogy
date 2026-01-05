from django.urls import path
from .views import author_profile

app_name = "acc_public_urls"

urlpatterns = [
    path("@<str:username>/", author_profile, name="author_profile"),
]
