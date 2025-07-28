"""
@admin.register(ExampleModel)
class ExampleModelAdmin(admin.ModelAdmin):
    list_display = ("field1", "field2", "created_at")
    list_editable = ("status",)
    readonly_fields = ("created_at", "updated_at")
    list_filter = ("status", "created_at")
    search_fields = ("field1", "field3")
    prepopulated_fields = {"slug_field": ("title_field",)}
    ordering = ("-created_at",)
    list_per_page = 20
    fieldsets = (
        (
            None,
            {
                "fields": ("field1", "field2"),
            },
        ),
        (
            'Advanced options',
            {
                "classes": ("collapse",),  # Collapsible section
                "fields": ("field3", "field4"),
            },
        ),
    )
    inlines = [
        # ExampleInlineAdmin,
    ]

class ExampleInlineAdmin(admin.TabularInline):  #or admin.StackedInline
    model = RelatedModel
    extra = 1
    fields = ("field1", "field2")
"""
from django.contrib import admin
from .models import *
# Register your models here.


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "icon_preview", "title", "is_read", "created_at")
    readonly_fields = ("created_at", "updated_at", "icon_preview")
    list_filter = ("created_at", "updated_at", "is_read")
    search_fields = ("id", "user__username", "title")
    list_per_page = 30
    fieldsets = (
        (
            None,
            {
                "fields": ("id",),
            },
        ),
        (
            'Notification Details',
            {
                "fields": ("user", "icon_preview", "icon", "title", "link", "is_read"),
            },
        ),
        (
            'Important Dates',
            {
                "fields": ("created_at", "updated_at"),
            },
        ),
    )
