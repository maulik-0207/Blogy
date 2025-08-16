from django.shortcuts import render
from django.http import HttpResponse


def create_post(request):
    
    ctx = {
        "title": "Create Post | Blogy",
    }
    return render(request, "posts/create_post.html", context= ctx)
