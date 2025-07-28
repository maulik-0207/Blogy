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
from django.core.exceptions import ValidationError
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
            return mark_safe(f'<img src="/media/{self.icon}" width="150" />')
        else:
            return mark_safe("<p>No Icon.</p>")
    
    def __str__(self) -> str:
        return f"{self.author.username} -> {self.title}"
    
    def __str__(self) -> str:
        return f"{self.user.username} | {self.title}"
    
    class Meta:
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"
        ordering = ["-created_at",]
