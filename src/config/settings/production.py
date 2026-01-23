from .base import *
import os

DEBUG = False

INSTALLED_APPS += [

]

MIDDLEWARE += [
    
]


PROFILE_IMAGE_MAX_SIZE = 2000000 # bytes - approx 2 mb
PROFILE_IMAGE_ALLOWED_EXTENSIONS = ['jpg','png','jpeg']

POST_THUMBNAIL_MAX_SIZE = 2000000 # bytes - approx 2 mb
POST_THUMBNAIL_ALLOWED_EXTENSIONS = ['jpg','png','jpeg']

POST_IMAGE_MAX_SIZE = 2000000 # bytes - approx 2 mb
POST_IMAGE_ALLOWED_EXTENSIONS = ['jpg','png','jpeg']

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {
            "level": "ERROR",
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR.parent.parent, 'logs', 'errors.log'),
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file"],
            "level": "ERROR",
            "propagate": True,
        },
    },
}
