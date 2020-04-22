"""
django:
    https://docs.djangoproject.com/en/3.0/ref/settings/#installed-apps
django-debug-toolbar:
    https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#prerequisites
django-extensions:
    https://django-extensions.readthedocs.io/en/latest/installation_instructions.html#configuration
"""

from ..general.installed_apps import INSTALLED_APPS

INSTALLED_APPS += ("debug_toolbar", "django_extensions")
