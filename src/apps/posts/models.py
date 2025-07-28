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
from .helper_func import get_post_thumbnail_path, get_post_image_path
from .validators import post_thumbnail_validator, post_image_validator
from django.core.exceptions import ValidationError
# Create your models here.

class Tag(models.Model):
    
    id = models.UUIDField(
        default= uuid4,
        primary_key= True,
        unique= True,
        null= False,
        blank= False,
        verbose_name= "ID",        
    )
    
    name = models.CharField(
        max_length= 255,
        verbose_name= "Name",
        blank= False,
        null= False,
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name= "Created At"
    )
    
    def __str__(self) -> str:
        return str(self.name)
    
    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"
        ordering = ["-created_at",]

class PostTag(models.Model):
    
    id = models.UUIDField(
        default= uuid4,
        primary_key= True,
        unique= True,
        null= False,
        blank= False,
        verbose_name= "ID",        
    )
    
    post = models.ForeignKey(
        to= "Post",
        related_name= "post_tags",
        on_delete=models.CASCADE,
        verbose_name= "Post",
    )
    
    tag = models.ForeignKey(
        to= Tag, 
        related_name= "tag_posts",
        on_delete=models.CASCADE,
        verbose_name= "Tag",
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name= "Created At",
    )
    
    def __str__(self) -> str:
        return f"{self.post.slug} -> {self.tag.name}"
    
    class Meta:
        verbose_name = "Post Tag"
        verbose_name_plural = "Post Tags"
        ordering = ["-created_at",]

class Post(models.Model):
    
    id = models.UUIDField(
        default= uuid4,
        primary_key= True,
        unique= True,
        null= False,
        blank= False,
        verbose_name= "ID",        
    )
    
    author = models.ForeignKey(
        to= get_user_model(),
        on_delete= models.CASCADE,
        verbose_name= "Author",
        related_name= "posts"
    )
    
    title = models.CharField(
        max_length= 160,
        verbose_name= "Title",
        error_messages= {
            "max_length": "Title is too long, Max Lengh is 160."
        },
        blank= False,
        null= False,
    )
    
    slug = models.SlugField(
        max_length= 165,
        verbose_name= "Slug",
        unique= True,
        blank= False,
        null= False
    )
    
    content = models.TextField(
        verbose_name= "Content",
    )
    
    table_of_content = models.TextField(
        verbose_name= "Table Of Content",
    )
    
    thumbnail = models.ImageField(
        upload_to=get_post_thumbnail_path,
        blank=True,
        null=True, 
        validators=[post_thumbnail_validator],
        verbose_name="Post Thumbnail",
    )
    
    tags = models.ManyToManyField(
        to= Tag,
        through= PostTag,
        verbose_name= "Tags",
    )
    
    read_time = models.DurationField(
        verbose_name= "Read Time",
        null = True,
        blank = True,
    )
    
    likes_count = models.PositiveIntegerField(
        default= 0,
        verbose_name= "Likes",
    )
    
    comments_count = models.PositiveIntegerField(
        default= 0,
        verbose_name= "Comments",
    )
    
    is_private = models.BooleanField(
        default= True,
        verbose_name= "Is Private?"
    )
    
    is_banned = models.BooleanField(
        default= False,
        verbose_name= "Is Banned?",
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name= "Created At"
    )
    
    updated_at = models.DateTimeField(
        verbose_name= "Updated At"
    )


    # def clean(self):
    #     super().clean()

    #     # if condition:
    #         # raise ValidationError({"field_name": "Error Message."})
    
    # def save(self, *args, **kwargs):
        
    #     # Do some changes if required
    #     # if self.char_field:
    #     #     self.char_field = self.char_field.capitalize()

    #     super().save(*args, **kwargs)
    
    @property
    def thumbnail_preview(self):
        if self.thumbnail:
            return mark_safe(f'<img src="/media/{self.thumbnail}" width="150" />')
        else:
            return mark_safe("<p>No Image.</p>")
    
    def __str__(self) -> str:
        return f"{self.author.username} -> {self.title}"
    
    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"
        ordering = ["-created_at",]

class PostLike(models.Model):
    
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
        related_name= "liked_posts"
    )
    
    post = models.ForeignKey(
        to= Post,
        on_delete= models.CASCADE,
        verbose_name= "Post",
        related_name= "likes"
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name= "Created At"
    )
    
    def __str__(self) -> str:
        return f"{self.user.username} likes {self.post.slug}"
    
    class Meta:
        verbose_name = "Post Like"
        verbose_name_plural = "Post Likes"
        unique_together = ['user', 'post']
        ordering = ["-created_at",]

class PostView(models.Model):
    
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
        related_name= "viewed_posts",
        blank= True,
        null= True
    )
    
    post = models.ForeignKey(
        to= Post,
        on_delete= models.CASCADE,
        verbose_name= "Post",
        related_name= "views"
    )
    
    ip_address = models.GenericIPAddressField(
        verbose_name= "IP Address",
    )
    
    user_agent = models.TextField(
        verbose_name= "User-Agent",
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name= "Created At"
    )
    
    def __str__(self) -> str:
        return f"{self.user.usernmae} viewed {self.post.slug}"
    
    class Meta:
        verbose_name = "Post View"
        verbose_name_plural = "Post Views"
        ordering = ["-created_at",]

class PostImage(models.Model):
    
    id = models.UUIDField(
        default= uuid4,
        primary_key= True,
        unique= True,
        null= False,
        blank= False,
        verbose_name= "ID",        
    )
    
    post = models.ForeignKey(
        to= Post,
        on_delete= models.CASCADE,
        verbose_name= "Post",
        related_name= "post_images"
    )
    
    image = models.ImageField(
        upload_to=get_post_image_path,
        blank=True,
        null=True, 
        validators=[post_image_validator],
        verbose_name="Post Image",
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name= "Created At"
    )
    
    @property
    def image_preview(self):
        if self.image:
            return mark_safe(f'<img src="/media/{self.image}" width="150" />')
        else:
            return mark_safe("<p>No Image.</p>")
    
    def __str__(self) -> str:
        return f"{self.post.title} | {self.id}"
    
    class Meta:
        verbose_name = "Post Image"
        verbose_name_plural = "Post Images"
        ordering = ["-created_at",]
