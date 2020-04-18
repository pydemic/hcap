"""
django:
    https://docs.djangoproject.com/en/3.0/topics/email/
    https://docs.djangoproject.com/en/3.0/ref/settings/#email-backend
"""

EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
