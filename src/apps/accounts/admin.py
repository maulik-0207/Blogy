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
from django.contrib.auth.admin import UserAdmin
# Register your models here.


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("id", "username", "email", "profile_image_preview", "followers_count", "followings_count", "is_verified")
    readonly_fields = ("profile_image_preview", "date_joined", "last_login")
    list_filter = ("is_active", "is_staff", "is_superuser", "is_verified", "is_banned", "date_joined", "last_login")
    search_fields = ("id", "username", "email", "name")
    list_per_page = 30
    fieldsets = (
        (
            None,
            {
                "fields": ("id",),
            },
        ),
        (
            'User Details',
            {
                "fields": ("username", "email", "name", "profile_image_preview", "profile_image", "bio", "followers_count", "followings_count"),
            },
        ),
        (
            'Security',
            {
                "fields": ("password", "uuid"),
            },
        ),
        (
            'Status',
            {
                "fields": ("is_verified", "is_banned", "is_active", "is_staff" ,"is_superuser"),
            },
        ),
        (
            'Important Dates',
            {
                "fields": ("last_login", "date_joined"),
            },
        ),
        (
            'Groups & Permissions',
            {
                "fields": ("groups", "user_permissions"),
            },
        ),
    )
    
@admin.register(UserFollow)
class UserFollowAdmin(admin.ModelAdmin):
    list_display = ("id", "follower", "following", "created_at")
    readonly_fields = ("created_at",)
    list_filter = ("created_at",)
    search_fields = ("id", "follower__username")
    list_per_page = 30
    fieldsets = (
        (
            None,
            {
                "fields": ("id",),
            },
        ),
        (
            'Follow Details',
            {
                "fields": ("follower", "following"),
            },
        ),
        (
            'Important Dates',
            {
                "fields": ("created_at",),
            },
        )
    )
