"""
django:
    https://docs.djangoproject.com/en/3.0/topics/http/middleware/
    https://docs.djangoproject.com/en/3.0/ref/settings/#middleware
django-debug-toolbar:
    https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#enabling-middleware
"""

from ..general.middleware import MIDDLEWARE

MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]
