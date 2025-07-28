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


@admin.register(UserReport)
class UserReportAdmin(admin.ModelAdmin):
    list_display = ("id", "reported_by", "reported_to", "subject", "is_reviewed")
    readonly_fields = ("created_at", "updated_at")
    list_filter = ("is_reviewed", "created_at", "updated_at")
    search_fields = ("id", "subject", "reported_to__username")
    list_per_page = 30
    fieldsets = (
        (
            None,
            {
                "fields": ("id",),
            },
        ),
        (
            'User Report Details',
            {
                "fields": ("reported_by", "reported_to", "subject", "description"),
            },
        ),
        (
            'Report Review',
            {
                "fields": ("is_reviewed", "reviewed_by", "action"),
            },
        ),
        (
            'Important Dates',
            {
                "fields": ("created_at", "updated_at"),
            },
        ),
    )

@admin.register(PostReport)
class PostReportAdmin(admin.ModelAdmin):
    list_display = ("id", "reported_by", "reported_post", "subject", "is_reviewed")
    readonly_fields = ("created_at", "updated_at")
    list_filter = ("is_reviewed", "created_at", "updated_at")
    search_fields = ("id", "subject", "reported_post__id")
    list_per_page = 30
    fieldsets = (
        (
            None,
            {
                "fields": ("id",),
            },
        ),
        (
            'User Report Details',
            {
                "fields": ("reported_by", "reported_post", "subject", "description"),
            },
        ),
        (
            'Report Review',
            {
                "fields": ("is_reviewed", "reviewed_by", "action"),
            },
        ),
        (
            'Important Dates',
            {
                "fields": ("created_at", "updated_at"),
            },
        ),
    )
    
@admin.register(CommentReport)
class CommentReportAdmin(admin.ModelAdmin):
    list_display = ("id", "reported_by", "reported_comment", "subject", "is_reviewed")
    readonly_fields = ("created_at", "updated_at")
    list_filter = ("is_reviewed", "created_at", "updated_at")
    search_fields = ("id", "subject", "reported_comment__id")
    list_per_page = 30
    fieldsets = (
        (
            None,
            {
                "fields": ("id",),
            },
        ),
        (
            'User Report Details',
            {
                "fields": ("reported_by", "reported_comment", "subject", "description"),
            },
        ),
        (
            'Report Review',
            {
                "fields": ("is_reviewed", "reviewed_by", "action"),
            },
        ),
        (
            'Important Dates',
            {
                "fields": ("created_at", "updated_at"),
            },
        ),
    )
