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
from django.db.models.signals import (
    pre_save,
    pre_delete
)
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.core.files.storage import default_storage
# Create your Signals here.


@receiver(pre_save, sender=get_user_model())
def delete_old_profile_image(sender, instance, **kwargs):
    
    if not instance.pk:
        return False

    try:
        old_instance = sender.objects.get(pk=instance.pk)
    except (sender.DoesNotExist, ValueError):
        return False

    if not old_instance.profile_image:
        return False

    if old_instance.profile_image != instance.profile_image:
        # Delete the old profile image file
        old_image_path = old_instance.profile_image.path
        if default_storage.exists(old_image_path):
            default_storage.delete(old_image_path)
            
@receiver(pre_delete, sender=get_user_model())
def delete_profile_image(sender, instance, **kwargs):
    
    if not instance.pk:
        return False
    
    if instance.profile_image:
        instance.profile_image.delete()
