"""
class Model(models.Model):
    
    id = models.UUIDField(
        default= uuid4,
        primary_key= True,
        unique= True,
        null= False,
        blank= False,
        verbose_name= "ID",        
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name= "Created At"
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name= "Updated At"
    )


    def clean(self):
        super().clean()

        # if condition:
            # raise ValidationError({"field_name": "Error Message."})
    
    def save(self, *args, **kwargs):
        
        # Do some changes if required
        # if self.char_field:
        #     self.char_field = self.char_field.capitalize()

        super().save(*args, **kwargs)
    
    def __str__(self) -> str:
        return str(self.id)
    
    class Meta:
        verbose_name = "Model"
        verbose_name_plural = "Models"
        ordering = ["-created_at",]
"""
from uuid import uuid4
from django.db import models
from django.utils.html import mark_safe
from django.contrib.auth import get_user_model
from apps.comments.models import Comment
from django.urls import reverse_lazy
from apps.posts.models import Post
from apps.post_lists.models import PostList
# Create your models here.


class Notification(models.Model):
    
    id = models.UUIDField(
        default= uuid4,
        primary_key= True,
        unique= True,
        null= False,
        blank= False,
        verbose_name= "ID",        
    )
    
    user = models.ForeignKey(
        to= get_user_model(),
        on_delete= models.CASCADE,
        verbose_name= "User",
        blank= False,
        null= False,
        related_name= "notifications"
    )
    
    icon = models.CharField(
        max_length= 300,
        verbose_name= "Icon Path",
        blank= True,
        null= True,
    )
    
    title = models.CharField(
        max_length= 500,
        verbose_name= "Title",
        blank= False,
        null= False,
    )
    
    link = models.URLField(
        verbose_name= "Link",
        blank= True,
        null= True,
    )
    
    is_read = models.BooleanField(
        default= False,
        verbose_name= "Is Read?",
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name= "Created At"
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name= "Updated At"
    )
    
    @property
    def icon_preview(self):
        if self.icon:
            return mark_safe(f'<img src="{self.icon}" width="150" />')
        else:
            return mark_safe("<p>No Icon.</p>")
    
    def __str__(self) -> str:
        return f"{self.user.username} -> {self.title}"
    
    class Meta:
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"
        ordering = ["-created_at",]


class NotificationService:

    @staticmethod
    def create_comment_notification(user, comment_obj: Comment, post_obj: Post):
        link = reverse_lazy(
            "comments:all_comments",
            kwargs={"slug": post_obj.slug}
        )

        # Reply to a comment
        if comment_obj.parent:
            parent_user = comment_obj.parent.user

            if parent_user != user:
                Notification.objects.create(
                    user=parent_user,
                    title=f"{user.username} replied to your comment",
                    link=link
                )

        # New comment on post
        else:
            if post_obj.author != user:
                Notification.objects.create(
                    user=post_obj.author,
                    title=f"{user.username} commented on your post",
                    link=link
                )

    @staticmethod
    def create_post_like_notification(user, post_obj: Post):
        if post_obj.author == user:
            return  # no self-like notification

        Notification.objects.create(
            user=post_obj.author,
            title=f"{user.username} liked your post",
            link=reverse_lazy(
                "posts:post_detail",
                kwargs={"slug": post_obj.slug}
            )
        )
        
    @staticmethod
    def create_post_list_like_notification(user, post_list: PostList):
        if post_list.user == user:
            return  # no self-like notification

        Notification.objects.create(
            user=post_list.user,
            title=f"{user.username} liked your post list",
            link=reverse_lazy(
                "post_lists:post_list_detail",
                kwargs={"pk": post_list.id}
            )
        )

    @staticmethod
    def create_comment_like_notification(user, comment_obj: Comment):
        if comment_obj.user == user:
            return  # no self-like notification

        Notification.objects.create(
            user=comment_obj.user,
            title=f"{user.username} liked your comment",
            link=reverse_lazy(
                "comments:all_comments",
                kwargs={"slug": comment_obj.post.slug}
            )
        )

    @staticmethod
    def create_follow_notification(follower, following):
        if follower == following:
            return

        Notification.objects.create(
            user=following,
            title=f"{follower.username} started following you",
            link=reverse_lazy(
                "acc_public_urls:author_profile",
                kwargs={"username": follower.username}
            )
        )

    @staticmethod
    def create_follow_back_notification(follower, following):
        """
        follower = the user who followed back
        following = the original follower
        """
        if follower == following:
            return

        Notification.objects.create(
            user=following,
            title=f"{follower.username} followed you back",
            link=reverse_lazy(
                "acc_public_urls:author_profile",
                kwargs={"username": follower.username}
            )
        )
