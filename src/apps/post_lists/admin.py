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


@admin.register(PostList)
class PostListAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "title", "likes", "created_at")
    readonly_fields = ("created_at", "updated_at")
    list_filter = ("created_at", "updated_at")
    search_fields = ("id", "user__username", "title")
    list_per_page = 50
    fieldsets = (
        (
            None,
            {
                "fields": ("id",),
            },
        ),
        (
            'Post List Details',
            {
                "fields": ("user", "title", "likes"),
            },
        ),
        (
            'Important Dates',
            {
                "fields": ("created_at", "updated_at"),
            },
        ),
    )

@admin.register(PostListItem)
class PostListItemAdmin(admin.ModelAdmin):
    list_display = ("id", "post_list", "post", "order", "created_at")
    readonly_fields = ("created_at",)
    list_filter = ("created_at",)
    search_fields = ("id", "post_list__title", "post__title")
    list_per_page = 50
    fieldsets = (
        (
            None,
            {
                "fields": ("id",),
            },
        ),
        (
            'Post List Item Details',
            {
                "fields": ("post_list", "post", "order"),
            },
        ),
        (
            'Important Dates',
            {
                "fields": ("created_at",),
            },
        ),
    )

@admin.register(PostListLike)
class PostListLikeAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "post_list", "created_at")
    readonly_fields = ("created_at",)
    list_filter = ("created_at",)
    search_fields = ("id", "user__username", "post_list__title")
    list_per_page = 50
    fieldsets = (
        (
            None,
            {
                "fields": ("id",),
            },
        ),
        (
            'Post List Like Details',
            {
                "fields": ("user", "post_list"),
            },
        ),
        (
            'Important Dates',
            {
                "fields": ("created_at",),
            },
        ),
    )
