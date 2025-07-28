"""
---> Model Signals <---
    
    Args:
        sender (Model): The model class.
        instance (Model instance): The instance being saved.
        created (in post_save only)(bool): True if a new instance was created, False if updated.
        kwargs: Additional keyword arguments.
    
@receiver(pre_save, sender = MyModel) #or pre_delete, post_delete 
def pre_save_handler(sender, instance, **kwargs):
    pass


@receiver(post_save, sender = MyModel)
def post_save_handler(sender, instance, created, **kwargs):
    pass
"""
from .models import * 
from django.db.models.signals import (
    pre_save,
    pre_delete
)
from django.dispatch import receiver
from django.core.files.storage import default_storage
# Create your Signals here.


@receiver(pre_save, sender=Post)
def delete_old_post_thumbnail(sender, instance, **kwargs):
    
    if not instance.pk:
        return False

    try:
        old_instance = sender.objects.get(pk=instance.pk)
    except (sender.DoesNotExist, ValueError):
        return False

    if not old_instance.thumbnail:
        return False

    if old_instance.thumbnail != instance.thumbnail:
        # Delete the old profile image file
        old_image_path = old_instance.thumbnail.path
        if default_storage.exists(old_image_path):
            default_storage.delete(old_image_path)
            
@receiver(pre_delete, sender=Post)
def delete_post_thumbnail(sender, instance, **kwargs):
    
    if not instance.pk:
        return False
    
    if instance.thumbnail:
        instance.thumbnail.delete()

@receiver(pre_save, sender=PostImage)
def delete_old_post_image(sender, instance, **kwargs):
    
    if not instance.pk:
        return False

    try:
        old_instance = sender.objects.get(pk=instance.pk)
    except (sender.DoesNotExist, ValueError):
        return False

    if not old_instance.image:
        return False

    if old_instance.image != instance.image:
        # Delete the old profile image file
        old_image_path = old_instance.image.path
        if default_storage.exists(old_image_path):
            default_storage.delete(old_image_path)
            
@receiver(pre_delete, sender=PostImage)
def delete_post_image(sender, instance, **kwargs):
    
    if not instance.pk:
        return False
    
    if instance.image:
        instance.image.delete()
