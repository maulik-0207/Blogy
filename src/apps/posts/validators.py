"""
def validate_even(value):
    if value % 2 != 0:
        raise ValidationError(
            f'number({value}) is not even',
            code='invalid_number'
        )
"""
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions
# Create your Validators here.

def post_thumbnail_validator(image):
    dimensions = get_image_dimensions(image)
    extension = image.name.split('.')[-1]
    
    if image.size > settings.POST_THUMBNAIL_MAX_SIZE:
        mb=settings.POST_THUMBNAIL_MAX_SIZE/1000000
        raise ValidationError(
            f"Image size must be less than {mb}MB.",
            code='invalid_image_size',
        )
    
    # if dimensions[0] < 360:
    #     raise ValidationError(
    #         "Minimun width and height is 360px.",
    #         code='invalid_image_dimension',
    #     )
    
    # if dimensions[0] != dimensions[1]:
    #     raise ValidationError(
    #         "Width and Height of Image must be same.",
    #         code='invalid_image_dimensions',
    #     )
    
    if extension not in settings.POST_THUMBNAIL_ALLOWED_EXTENSIONS:
        raise ValidationError(
            f".{extension} extension is not allowed.",
            code='invalid_image_extension',
        )

def post_image_validator(image):
    extension = image.name.split('.')[-1]
    
    if image.size > settings.POST_IMAGE_MAX_SIZE:
        mb=settings.POST_IMAGE_MAX_SIZE/1000000
        raise ValidationError(
            f"Image size must be less than {mb}MB.",
            code='invalid_image_size',
        )
    
    if extension not in settings.POST_IMAGE_ALLOWED_EXTENSIONS:
        raise ValidationError(
            f".{extension} extension is not allowed.",
            code='invalid_image_extension',
        )
