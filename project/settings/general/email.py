"""
django:
    https://docs.djangoproject.com/en/3.0/topics/email/
    https://docs.djangoproject.com/en/3.0/ref/settings/#default-from-email
    https://docs.djangoproject.com/en/3.0/ref/settings/#email-backend
"""

from ..env import env
from .paths import BASE_DIR

DEFAULT_FROM_EMAIL = env("HC__DEFAULT_FROM_EMAIL", default="you@domain.com")

EMAIL_TYPE = env("HC__EMAIL_MODE", default="console")

if EMAIL_TYPE == "smtp":
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = env("HC__EMAIL_HOST")
    EMAIL_PORT = env("HC__EMAIL_PORT", default=587)
    EMAIL_HOST_USER = env("HC__EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = env("HC__EMAIL_HOST_PASSWORD")
    EMAIL_USE_TLS = True
    EMAIL_TIMEOUT = 20
elif EMAIL_TYPE == "console":
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
elif EMAIL_TYPE == "file":
    EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
