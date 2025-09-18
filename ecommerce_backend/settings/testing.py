# ecommerce_backend/settings/testing.py

import logging

from .base import *


DEBUG = False
TESTING = True

# Disable rate limiting during testing
REST_FRAMEWORK.update(
    {
        "DEFAULT_THROTTLE_CLASSES": [],
        "DEFAULT_THROTTLE_RATES": {
            "anon": None,
            "user": None,
            "register": None,
            "login": None,
        },
        "TEST_REQUEST_DEFAULT_FORMAT": "json",
    },
)

# Use faster password hasher for testing
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]

# Use in-memory SQLite for faster tests
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    },
}

# Disable email sending during tests
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

# Disable logging during tests
logging.disable(logging.CRITICAL)

# Disable cache for tests
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
    },
    "sessions": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    },
}

# CORS settings for testing
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # Default React dev server
    "http://127.0.0.1:3000",  # Alternative localhost
]
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_ALL_ORIGINS = False  # For security, only allow the origins listed above

# For testing, we can also allow all origins if needed
# CORS_ALLOW_ALL_ORIGINS = True  # Uncomment if you need to allow all origins during testing

# Configure session engine to use cache
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "sessions"

# Celery
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True
