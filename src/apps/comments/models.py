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
from django.contrib.auth import get_user_model
from apps.posts.models import Post
from django.core.exceptions import ValidationError
# Create your models here.


class Comment(models.Model):
    
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
        related_name= "commented_posts"
    )
    
    post = models.ForeignKey(
        to= Post,
        on_delete= models.CASCADE,
        verbose_name= "Post",
        blank= False,
        null= False,
        related_name="comments"
    )
    
    content = models.TextField(
        max_length= 2000,
        verbose_name= "Content",
    )
    
    parent = models.ForeignKey(
        to= 'self',
        on_delete= models.CASCADE,
        verbose_name= "Parent",
        blank= True,
        null= True,
        related_name= "replies",
    )
    
    likes = models.PositiveIntegerField(
        default= 0,
        verbose_name= "Likes",
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name= "Created At"
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name= "Updated At"
    )
    
    def __str__(self) -> str:
        return f"{self.user.username} commented on {self.post.title}"
    
    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
        ordering = ["-created_at",]

class CommentLike(models.Model):
    
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
        on_delete=models.CASCADE,
        verbose_name= "User",
        blank= False,
        null= False,
        related_name= "liked_comments",
    )
    
    comment = models.ForeignKey(
        to= Comment, 
        on_delete=models.CASCADE,
        verbose_name= "Comment",
        blank= False,
        null= False,
        related_name= "comment_likes"
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name= "Created At"
    )
    
    def __str__(self) -> str:
        return f"{self.user.username} liked comment:{self.comment[:20]}"

    class Meta:
        verbose_name = "Comment Like"
        verbose_name_plural = "Comment Likes"
        ordering = ["-created_at",]
        unique_together = ('comment', 'user')
