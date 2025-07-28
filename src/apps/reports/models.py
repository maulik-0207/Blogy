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
from apps.comments.models import Comment
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
# Create your models here.


class UserReport(models.Model):
    
    id = models.UUIDField(
        default= uuid4,
        primary_key= True,
        unique= True,
        null= False,
        blank= False,
        verbose_name= "ID",        
    )
    
    reported_by = models.ForeignKey(
        to= get_user_model(),
        on_delete= models.CASCADE,
        verbose_name= "Reported By",
        blank= False,
        null= False,
        related_name= "reported_users"
    )
    
    reported_to = models.ForeignKey(
        to= get_user_model(),
        on_delete= models.CASCADE,
        verbose_name= "Reported To",
        blank= False,
        null= False,
        related_name= "user_reports"
    )
    
    subject = models.CharField(
        max_length= 400,
        verbose_name= "Subject",
        blank= False,
        null= False,
    )
    
    description = models.CharField(
        max_length= 1000,
        verbose_name= "Description",
        blank= True,
        null= True,
    )
    
    is_reviewed = models.BooleanField(
        default= False,
        verbose_name= "Is Reviewed?"
    )
    
    reviewed_by = models.ForeignKey(
        to= get_user_model(),
        on_delete= models.CASCADE,
        verbose_name= "Reviewed By",
        blank= True,
        null= True,
        related_name= "reviewed_user_reports"
    )
    
    action = models.CharField(
        max_length= 200,
        verbose_name= "Action",
        blank= True,
        null= True,
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
        return f"{self.reported_by.username} reports to {self.reported_to.username} for {self.subject}."
    
    class Meta:
        verbose_name = "User Report"
        verbose_name_plural = "User Reports"
        ordering = ["-created_at",]
    
class PostReport(models.Model):
    
    id = models.UUIDField(
        default= uuid4,
        primary_key= True,
        unique= True,
        null= False,
        blank= False,
        verbose_name= "ID",        
    )
    
    reported_by = models.ForeignKey(
        to= get_user_model(),
        on_delete= models.CASCADE,
        verbose_name= "Reported By",
        blank= False,
        null= False,
        related_name= "reported_posts"
    )
    
    reported_post = models.ForeignKey(
        to= Post,
        on_delete= models.CASCADE,
        verbose_name= "Reported Post",
        blank= False,
        null= False,
        related_name= "post_reports"
    )
    
    subject = models.CharField(
        max_length= 400,
        verbose_name= "Subject",
        blank= False,
        null= False,
    )
    
    description = models.CharField(
        max_length= 1000,
        verbose_name= "Description",
        blank= True,
        null= True,
    )
    
    is_reviewed = models.BooleanField(
        default= False,
        verbose_name= "Is Reviewed?"
    )
    
    reviewed_by = models.ForeignKey(
        to= get_user_model(),
        on_delete= models.CASCADE,
        verbose_name= "Reviewed By",
        blank= True,
        null= True,
        related_name= "reviewed_post_reports"
    )
    
    action = models.CharField(
        max_length= 200,
        verbose_name= "Action",
        blank= True,
        null= True,
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
        return f"{self.reported_by.username} reports to {self.reported_post.title} for {self.subject}."
    
    class Meta:
        verbose_name = "Post Report"
        verbose_name_plural = "Post Reports"
        ordering = ["-created_at",]

class CommentReport(models.Model):
    
    id = models.UUIDField(
        default= uuid4,
        primary_key= True,
        unique= True,
        null= False,
        blank= False,
        verbose_name= "ID",        
    )
    
    reported_by = models.ForeignKey(
        to= get_user_model(),
        on_delete= models.CASCADE,
        verbose_name= "Reported By",
        blank= False,
        null= False,
        related_name= "reported_comments"
    )
    
    reported_comment = models.ForeignKey(
        to= Comment,
        on_delete= models.CASCADE,
        verbose_name= "Reported Comment",
        blank= False,
        null= False,
        related_name= "comment_reports"
    )
    
    subject = models.CharField(
        max_length= 400,
        verbose_name= "Subject",
        blank= False,
        null= False,
    )
    
    description = models.CharField(
        max_length= 1000,
        verbose_name= "Description",
        blank= True,
        null= True,
    )
    
    is_reviewed = models.BooleanField(
        default= False,
        verbose_name= "Is Reviewed?"
    )
    
    reviewed_by = models.ForeignKey(
        to= get_user_model(),
        on_delete= models.CASCADE,
        verbose_name= "Reviewed By",
        blank= True,
        null= True,
        related_name= "reviewed_comment_reports"
    )
    
    action = models.CharField(
        max_length= 200,
        verbose_name= "Action",
        blank= True,
        null= True,
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
        return f"{self.reported_by.username} reports to {self.reported_comment.pk} for {self.subject}."
    
    class Meta:
        verbose_name = "Comment Report"
        verbose_name_plural = "Comment Reports"
        ordering = ["-created_at",]
