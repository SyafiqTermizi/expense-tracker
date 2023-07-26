from .base import *

DEBUG = False

MIDDLEWARE = list(
    set(
        [
            "django.middleware.security.SecurityMiddleware",
            "whitenoise.middleware.WhiteNoiseMiddleware",
            *MIDDLEWARE,
        ]
    )
)
