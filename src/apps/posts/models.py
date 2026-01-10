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
from django.core.validators import FileExtensionValidator
from django.conf import settings
from django.utils.timezone import now
from datetime import timedelta
from bs4 import BeautifulSoup
from typing import Tuple
import random
from django.utils.html import escape
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
        ordering = ["created_at",]
        constraints =[
            models.UniqueConstraint(
                fields= ['post', 'tag'],
                name= 'unique_post_tag'
            )
        ]

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
        blank= True,
        null= True
    )
    
    table_of_content = models.TextField(
        verbose_name= "Table Of Content",
        blank= True,
        null= True,
    )
    
    thumbnail = models.ImageField(
        upload_to=get_post_thumbnail_path,
        blank=True,
        null=True, 
        validators=[post_thumbnail_validator, FileExtensionValidator(settings.POST_THUMBNAIL_ALLOWED_EXTENSIONS)],
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
        default= timedelta(seconds=0)
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
        verbose_name= "Updated At",
        default= now,
    )

    def set_tags(self, tags:str):
        old_tags = [str(tag.tag.name) for tag in self.post_tags.all()]
        new_tags = [tag.lower().strip() for tag in tags.split(",")]
        
        total_tags = 0
        for tag in new_tags:
            if tag not in old_tags and tag != "":
                tag_obj = Tag.objects.get_or_create(name = tag)[0]
                PostTag.objects.create(post = self, tag= tag_obj)
                total_tags += 1
            elif tag in old_tags:
                total_tags += 1
            
            if total_tags >= 5:
                break
        
        for tag in old_tags:
            if tag not in new_tags:
                postTag_obj = PostTag.objects.get(post = self, tag__name = tag)
                postTag_obj.delete()

    def generate_table_of_content_html(self) -> Tuple[str, str]:
        """
        - Injects id into h1–h4 headings
        - Generates HTML TOC with anchor links
        - Returns (updated_content, toc_html)
        """

        if not self.content:
            return self.content, ""

        soup = BeautifulSoup(self.content, "html.parser")
        headings = soup.find_all(["h1", "h2", "h3", "h4"])

        if not headings:
            return self.content, ""

        toc_html = [
            '<ul class="space-y-2 text-sm">'
        ]

        previous_level = 1

        for heading in headings:
            level = int(heading.name[1])  # h2 → 2
            text = heading.get_text(strip=True)

            if not text:
                continue

            hid  = "".join(random.choice("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz") for _ in range(8))
            heading["id"] = hid

            text_escaped = escape(text)

            # Nesting logic
            while level > previous_level:
                toc_html.append('<ul class="ml-4 space-y-1">')
                previous_level += 1

            while level < previous_level:
                toc_html.append("</ul>")
                previous_level -= 1

            # 🎯 h2 = main tab
            if level == 1:
                # h1 → special
                toc_html.append(
                    f'''
                    <li>
                        <a href="#{hid}"
                        class="block px-3 py-2 rounded-lg
                                font-semibold text-gray-900
                                hover:bg-indigo-50 hover:text-indigo-600">
                            {text_escaped}
                        </a>
                    </li>
                    '''
                )
            elif level == 2:
                toc_html.append(
                    f'''
                    <li>
                        <a href="#{hid}"
                           class="block px-3 py-2 rounded-lg
                                  font-medium text-gray-800
                                  hover:bg-indigo-50 hover:text-indigo-600
                                  transition">
                            {text_escaped}
                        </a>
                    </li>
                    '''
                )
            else:
                toc_html.append(
                    f'''
                    <li>
                        <a href="#{hid}"
                           class="block px-3 py-1 text-gray-600
                                  hover:text-indigo-600 transition">
                            {text_escaped}
                        </a>
                    </li>
                    '''
                )

        while previous_level > 2:
            toc_html.append("</ul>")
            previous_level -= 1

        toc_html.append("</ul>")

        return str(soup), "".join(toc_html)
    
    def remove_unused_post_images(self):
        postImage_objs = PostImage.objects.filter(post = self)
        
        image_urls = []
        soup = BeautifulSoup(self.content,'html.parser')
        img_tags = soup.find_all('img')
        for img_tag in img_tags:
            if 'src' in img_tag.attrs:
                img_url = str(img_tag['src']).split("?")[0]
                print(img_url)
                image_urls.append(img_url)
                
        for postImage_obj in postImage_objs:
            print(postImage_obj.image.url)
            if postImage_obj.image.url not in image_urls:
                postImage_obj.delete()
        
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
        constraints =[
            models.UniqueConstraint(
                fields= ['user', 'post'],
                name= 'unique_post_like'
            )
        ]
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
        user = self.user.username if self.user else self.ip_address
        return f"{user} viewed {self.post.slug}"
    
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
        validators=[post_image_validator, FileExtensionValidator(settings.POST_IMAGE_ALLOWED_EXTENSIONS)],
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
