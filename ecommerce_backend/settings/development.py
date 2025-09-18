# ecommerce_backend/settings/development.py

from .base import *


DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

# Email backend for development
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

ENVIRONMENT = (env("ENVIRONMENT", default="development"),)
