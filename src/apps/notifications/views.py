from django.shortcuts import render
from django.http import HttpResponse


def example_view(request):
    
    ctx = {
        "title": "Page Title Here",
    }
    return render(request, "notifications/example_template.html", context= ctx)
