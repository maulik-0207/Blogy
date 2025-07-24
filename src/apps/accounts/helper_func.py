import os
import random
from datetime import date

def get_profile_image_path(instance, filename):
    file = filename.split(".")
    
    random_string = "".join(random.choice("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz") for _ in range(5))
    new_filename = f"Profile_Image_{random_string}.{file[1]}"

    today = date.today()

    return os.path.join('profile_images', str(today.year), str(today.month), new_filename)
