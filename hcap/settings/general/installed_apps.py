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

INSTALLED_APPS = (
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.sites",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Material
    "material",
    "material.frontend",
    "material.admin",
    # All auth
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    # Monitoring
    "django_prometheus",
    # General
    "compressor",
    "crispy_forms",
    "django_select2",
    # Apps
    "hcap",
    "hcap_accounts",
    "hcap_geo",
    "hcap_institutions",
    "hcap_monitors",
    "hcap_notifications",
    "hcap_utils",
)
