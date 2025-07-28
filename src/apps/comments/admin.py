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


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "post", "parent", "likes", "created_at")
    readonly_fields = ("created_at", "updated_at")
    list_filter = ("created_at", "updated_at")
    search_fields = ("id", "user__username", "post__title")
    list_per_page = 30
    fieldsets = (
        (
            None,
            {
                "fields": ("id",),
            },
        ),
        (
            'Comment Details',
            {
                "fields": ("user", "post", "content", "parent", "likes"),
            },
        ),
        (
            'Important Dates',
            {
                "fields": ("created_at", "updated_at"),
            },
        ),
    )

@admin.register(CommentLike)
class CommentLikeAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "comment", "created_at")
    readonly_fields = ("created_at",)
    list_filter = ("created_at",)
    search_fields = ("id", "user__username", "comment__id")
    list_per_page = 50
    fieldsets = (
        (
            None,
            {
                "fields": ("id",),
            },
        ),
        (
            'Comment Like Details',
            {
                "fields": ("user", "comment"),
            },
        ),
        (
            'Important Dates',
            {
                "fields": ("created_at",),
            },
        ),
    )
