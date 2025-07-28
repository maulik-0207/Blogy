from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    
    ctx = {
        "title": "Home | Blogy",
    }
    return render(request, "index.html", context= ctx)
