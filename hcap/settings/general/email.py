"""
django:
    https://docs.djangoproject.com/en/3.0/topics/email/
    https://docs.djangoproject.com/en/3.0/ref/settings/#default-from-email
    https://docs.djangoproject.com/en/3.0/ref/settings/#email-backend
"""

from hcap.settings.env import env
from .paths import BASE_DIR

DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", default="you@domain.com")

EMAIL_TYPE = env("EMAIL_MODE", default="console")

if EMAIL_TYPE == "smtp":
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = env("EMAIL_HOST")
    EMAIL_PORT = env("EMAIL_PORT", default=587)
    EMAIL_HOST_USER = env("EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
    EMAIL_USE_TLS = True
    EMAIL_TIMEOUT = 20
elif EMAIL_TYPE == "console":
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
elif EMAIL_TYPE == "file":
    EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
