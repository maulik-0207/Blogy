"""
def validate_even(value):
    if value % 2 != 0:
        raise ValidationError(
            f'number({value}) is not even',
            code='invalid_number'
        )
"""
import re
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions
# Create your Validators here.


def username_validator(username):
    if len(username) < 3 or len(username) > 30:
        raise ValidationError(
            'Length of username must be 3 to 30.',
            code='invalid_username_length'
        )
    
    pattern = r'^[a-zA-Z][a-zA-Z0-9_-]*[a-zA-Z0-9]$'
    
    if not re.match(pattern, username):
        raise ValidationError(
            'Username must start with a letter, end with a letter/number & contain only letters, numbers, underscores(_) or hyphens(-).',
            code='invalid_username_pattern'
        )

def profile_image_validator(image):
    dimensions = get_image_dimensions(image)
    extension = image.name.split('.')[-1]
    
    if image.size > settings.PROFILE_IMAGE_MAX_SIZE:
        mb=settings.PROFILE_IMAGE_MAX_SIZE/1000000
        raise ValidationError(
            f"Image size must be less than {mb}MB.",
            code='invalid_image_size',
        )
    
    if dimensions[0] < 360:
        raise ValidationError(
            "Minimun width and height is 360px.",
            code='invalid_image_dimension',
        )
    
    if dimensions[0] != dimensions[1]:
        raise ValidationError(
            "Width and Height of Image must be same.",
            code='invalid_image_dimensions',
        )
    
    if extension not in settings.PROFILE_IMAGE_ALLOWED_EXTENSIONS:
        raise ValidationError(
            f".{extension} extension is not allowed.",
            code='invalid_image_extension',
        )
