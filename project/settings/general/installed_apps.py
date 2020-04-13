"""
django:
    https://docs.djangoproject.com/en/3.0/ref/settings/#installed-apps
django-allauth:
    https://django-allauth.readthedocs.io/en/latest/installation.html#django
django-compressor:
    https://django-compressor.readthedocs.io/en/stable/quickstart/#installation
django-crispy-forms:
    https://django-crispy-forms.readthedocs.io/en/latest/install.html#installing-django-crispy-forms
viewflow:
    http://docs.viewflow.io/material_forms.html#installation
    http://docs.viewflow.io/material_frontend.html#installation
"""

INSTALLED_APPS = [
    # Local
    "app",
    # Material
    "material",
    "material.frontend",
    "material.admin",
    # All auth
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    # User apps depends on locations and must migrate before allauth.account
    "users",
    "locations",
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.sites",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Monitoring
    "django_prometheus",
    # Others
    "compressor",
    "crispy_forms",
    "utils",
    "django_select2",
]
