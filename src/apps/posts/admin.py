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


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "created_at")
    readonly_fields = ("created_at",)
    list_filter = ("created_at",)
    search_fields = ("id", "name",)
    list_per_page = 50
    fieldsets = (
        (
            None,
            {
                "fields": ("id",),
            },
        ),
        (
            'Tag',
            {
                "fields": ("name",),
            },
        ),
        (
            'Important Dates',
            {
                "fields": ("created_at",),
            },
        ),
    )
    
@admin.register(PostTag)
class PostTagAdmin(admin.ModelAdmin):
    list_display = ("id", "post", "tag", "created_at")
    readonly_fields = ("created_at",)
    list_filter = ("tag", "created_at")
    search_fields = ("id", "post__title",)
    list_per_page = 50
    fieldsets = (
        (
            None,
            {
                "fields": ("id",),
            },
        ),
        (
            'Post Tag',
            {
                "fields": ("post", "tag"),
            },
        ),
        (
            'Important Dates',
            {
                "fields": ("created_at",),
            },
        ),
    )

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "title", "is_private", "thumbnail_preview")
    readonly_fields = ("thumbnail_preview", "created_at", "updated_at")
    list_filter = ("is_private", "is_banned","created_at", "updated_at")
    search_fields = ("id", "author__username", "title", "slug")
    list_per_page = 30
    fieldsets = (
        (
            None,
            {
                "fields": ("id",),
            },
        ),
        (
            'Post Details',
            {
                "fields": ("author", "slug", "title", "content", "table_of_content", "thumbnail_preview", "thumbnail", "read_time"),
            },
        ),
        (
            'Post Stats',
            {
                "fields": ("likes_count", "comments_count"),
            },
        ),
        (
            'Post Status',
            {
                "fields": ("is_private", "is_banned"),
            },
        ),
        (
            'Important Dates',
            {
                "fields": ("updated_at", "created_at"),
            },
        ),
    )
    
@admin.register(PostLike)
class PostLikeAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "post", "created_at")
    readonly_fields = ("created_at",)
    list_filter = ("created_at",)
    search_fields = ("id", "user__username", "post__slug")
    list_per_page = 50
    fieldsets = (
        (
            None,
            {
                "fields": ("id",),
            },
        ),
        (
            'Post Like Details',
            {
                "fields": ("user", "post"),
            },
        ),
        (
            'Important Dates',
            {
                "fields": ("created_at",),
            },
        ),
    )
    
@admin.register(PostView)
class PostViewAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "post", "ip_address", "user_agent", "created_at")
    readonly_fields = ("created_at",)
    list_filter = ("created_at",)
    search_fields = ("id", "ip_address", "user_agent", "user__username", "post__slug")
    list_per_page = 50
    fieldsets = (
        (
            None,
            {
                "fields": ("id",),
            },
        ),
        (
            'Post View Details',
            {
                "fields": ("user", "post", "ip_address", "user_agent"),
            },
        ),
        (
            'Important Dates',
            {
                "fields": ("created_at",),
            },
        ),
    )

@admin.register(PostImage)
class PostImageAdmin(admin.ModelAdmin):
    list_display = ("id", "post", "image_preview", "created_at")
    readonly_fields = ("created_at", "image_preview")
    list_filter = ("created_at",)
    search_fields = ("id", "post__title", "post__slug")
    list_per_page = 50
    fieldsets = (
        (
            None,
            {
                "fields": ("id",),
            },
        ),
        (
            'Post Image Details',
            {
                "fields": ("post", "image_preview", "image"),
            },
        ),
        (
            'Important Dates',
            {
                "fields": ("created_at",),
            },
        ),
    )
