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
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser
from .helper_func import get_profile_image_path
from .validators import username_validator, profile_image_validator
# Create your models here.


class User(AbstractUser):
    
    id = models.UUIDField(
        default= uuid4,
        primary_key= True,
        unique= True,
        null= False,
        blank= False,
        verbose_name= "ID",        
    )
    
    username = models.CharField(
        max_length=30,
        unique=True,
        error_messages= {
            "unique":"Username is not available.",
            "max_length":"Username is too long, Max - 30."
            },
        help_text = "a-Z, 0-9, underscore & hypen.",
        validators = [username_validator,],
        verbose_name="Username",
    )

    first_name = None
    last_name = None
    
    email  = models.EmailField(
        unique= True,
        blank= False,
        null= False,
        validators= [EmailValidator],
        error_messages= {
            "unique" : "An account is already registered with this Email Id.",
        },
        verbose_name="Email Id",
    )
    
    name = models.CharField(
        max_length= 150,
        verbose_name= "Name",
        blank= True,
        null= True,
    )
    
    profile_image = models.ImageField(
        upload_to=get_profile_image_path,
        blank=True,
        null=True, 
        validators=[profile_image_validator],
        verbose_name="Profile Image"
    )
    
    bio = models.TextField(
        verbose_name= "Bio",
        max_length= 3000,
    )
    
    followers = models.PositiveIntegerField(
        default= 0,
        verbose_name= "Followers",
    )
    
    followings = models.PositiveIntegerField(
        default= 0,
        verbose_name= "Followings",
    )
    
    is_verified = models.BooleanField(
        default= False,
        verbose_name= "Is Verified?"
    )
    
    is_banned = models.BooleanField(
        default= False,
        verbose_name= "Is Banned?"
    )

    uuid = models.UUIDField(
        blank= True,
        null= True,
        unique= True,
        verbose_name= "UUID",
    )
    
    @property
    def profile_image_preview(self):
        if self.profile_image:
            return mark_safe(f'<img src="/media/{self.profile_image}" width="150" height="150" />')
        else:
            return mark_safe("<p>No Image.</p>")
    
    def __str__(self) -> str:
        return str(self.username)
    
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["-date_joined",]
        
class UserFollow(models.Model):
    
    id = models.UUIDField(
        default= uuid4,
        primary_key= True,
        unique= True,
        null= False,
        blank= False,
        verbose_name= "ID",        
    )
    
    follower = models.ForeignKey(
        to= User,
        on_delete= models.CASCADE,
        related_name= "followings",
        verbose_name= "Follower",
        help_text= "User that follows."
    )
    
    following = models.ForeignKey(
        to= User,
        on_delete= models.CASCADE,
        related_name= "followers",
        verbose_name= "Following",
        help_text= "User that being Followed."
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name= "Created At"
    )
    
    def __str__(self) -> str:
        return f"{self.follower.username} -> {self.following.username}" 
    
    class Meta:
        verbose_name = "User Follow"
        verbose_name_plural = "User Follows"
        unique_together = ["follower", "following"]
        ordering = ["-created_at",]
    