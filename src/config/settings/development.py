from .base import *

DEBUG = True

INSTALLED_APPS += [
    'debug_toolbar',
]

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

INTERNAL_IPS = [
    "127.0.0.1",
]

AUTH_PASSWORD_VALIDATORS = []

PROFILE_IMAGE_MAX_SIZE = 2000000 # bytes - approx 2 mb
PROFILE_IMAGE_ALLOWED_EXTENSIONS = ['jpg','png','jpeg']

POST_THUMBNAIL_MAX_SIZE = 2000000 # bytes - approx 2 mb
POST_THUMBNAIL_ALLOWED_EXTENSIONS = ['jpg','png','jpeg']

POST_IMAGE_MAX_SIZE = 2000000 # bytes - approx 2 mb
POST_IMAGE_ALLOWED_EXTENSIONS = ['jpg','png','jpeg']
