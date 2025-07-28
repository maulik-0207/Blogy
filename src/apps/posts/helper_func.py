import os
import random
from datetime import date

def get_post_thumbnail_path(instance, filename):
    file = filename.split(".")
    
    random_string = "".join(random.choice("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz") for _ in range(8))
    new_filename = f"Post_Thumbnail_{random_string}.{file[1]}"

    today = date.today()

    return os.path.join('posts', 'thumbnails', str(today.year), str(today.month), new_filename)

def get_post_image_path(instance, filename):
    file = filename.split(".")
    
    random_string = "".join(random.choice("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz") for _ in range(8))
    new_filename = f"Post_Image_{random_string}.{file[1]}"

    today = date.today()

    return os.path.join('posts', 'images', str(today.year), str(today.month), new_filename)
