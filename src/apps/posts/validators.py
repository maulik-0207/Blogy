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
    width, height = get_image_dimensions(image)
    # extension = image.name.split('.')[-1]
    
    if image.size > settings.POST_THUMBNAIL_MAX_SIZE:
        mb=settings.POST_THUMBNAIL_MAX_SIZE/1000000
        raise ValidationError(
            f"Image size must be less than {mb}MB.",
            code='invalid_image_size',
        )
    
    expected_ratio = 16 / 9
    actual_ratio = width / height
    tolerance = 0.02
    
    if abs(actual_ratio - expected_ratio) > tolerance:
        raise ValidationError(
            "Thumbnail must have a 16:9 aspect ratio (e.g. 1280×720).",
            code="invalid_aspect_ratio",
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
    
    # if extension not in settings.POST_THUMBNAIL_ALLOWED_EXTENSIONS:
    #     raise ValidationError(
    #         f".{extension} extension is not allowed.",
    #         code='invalid_image_extension',
    #     )

def post_image_validator(image):
    # extension = image.name.split('.')[-1]
    
    if image.size > settings.POST_IMAGE_MAX_SIZE:
        mb=settings.POST_IMAGE_MAX_SIZE/1000000
        raise ValidationError(
            f"Image size must be less than {mb}MB.",
            code='invalid_image_size',
        )
    
    # if extension not in settings.POST_IMAGE_ALLOWED_EXTENSIONS:
    #     raise ValidationError(
    #         f".{extension} extension is not allowed.",
    #         code='invalid_image_extension',
    #     )
