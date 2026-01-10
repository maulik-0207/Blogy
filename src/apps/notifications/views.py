from django.shortcuts import render, get_object_or_404, redirect
from .models import Notification
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages


@login_required
def notification_list(request):
    notification_objs = Notification.objects.filter(user=request.user)

    paginator = Paginator(notification_objs, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    unread_ids = [
        n.id for n in page_obj if not n.is_read
    ]
    if unread_ids:
        Notification.objects.filter(id__in=unread_ids).update(is_read=True)

    ctx = {
        "title": "Notifications | Blogy",
        "page_obj": page_obj,
    }
    
    return render(request, "notifications/notification_list.html", ctx)

@login_required
def notification_delete(request, pk):
    notification_obj = get_object_or_404(
        Notification,
        pk=pk,
        user=request.user
    )

    if request.method == "POST":
        notification_obj.delete()
    invalid_redirect_urls = [
        '/accounts/logout/',
        '/accounts/register/',
        '/accounts/login/'
    ]
    messages.success(request, "Notification Deleted.")
    if request.POST.get("next") and request.POST.get("next") not in invalid_redirect_urls:
        return redirect(request.POST.get("next"))
    else:
        return redirect("notifications:notification_list")
