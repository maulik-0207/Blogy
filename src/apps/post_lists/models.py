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
from apps.posts.models import Post
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
# Create your models here.


class PostList(models.Model):
    
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
        related_name= "post_lists",
        blank= False,
        null= False,
    )
    
    title = models.CharField(
        max_length= 300,
        verbose_name= "Title",
        error_messages= {
            "max_length" : "Too long. Max - 300",
        },
        blank= False,
        null= False,
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
        verbose_name= "Updated At"
    )
    
    def __str__(self) -> str:
        return f"{self.user.username} made {self.title}"
    
    class Meta:
        verbose_name = "Post List"
        verbose_name_plural = "Post Lists"
        ordering = ["-created_at",]
    
class PostListItem(models.Model):
    
    id = models.UUIDField(
        default= uuid4,
        primary_key= True,
        unique= True,
        null= False,
        blank= False,
        verbose_name= "ID",        
    )
    
    post_list = models.ForeignKey(
        to= PostList,
        on_delete= models.CASCADE,
        verbose_name= "Post List",
        related_name= "post_list_items",
        blank= False,
        null= False,
    )
    
    post = models.ForeignKey(
        to= Post,
        on_delete= models.CASCADE,
        verbose_name= "Post",
        related_name= "list_items",
        blank= False,
        null= False,
    )
    
    order = models.PositiveIntegerField(
        verbose_name= "Order",
        default= 0,
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name= "Created At"
    )
    
    def __str__(self) -> str:
        return f"{self.post_list.title} has {self.post.title}"
    
    class Meta:
        verbose_name = "Post List Item"
        verbose_name_plural = "Post List Items"
        ordering = ["-created_at",]

class PostListLike(models.Model):
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
        related_name= "liked_lists",
        blank= False,
        null= False,
    )
    
    post_list = models.ForeignKey(
        to= PostList,
        on_delete= models.CASCADE,
        verbose_name= "Post List",
        related_name= "list_likes",
        blank= False,
        null= False,
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name= "Created At"
    )
    
    def __str__(self) -> str:
        return f"{self.user.username} likes {self.post_list.title}"
    
    class Meta:
        verbose_name = "Post List Like"
        verbose_name_plural = "Post List Likes"
        ordering = ["-created_at",]
