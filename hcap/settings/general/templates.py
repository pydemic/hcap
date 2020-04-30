"""
django:
    https://docs.djangoproject.com/en/3.0/ref/settings/#templates
"""

from .paths import TEMPLATE_DIRS

TEMPLATES = [
    {"BACKEND": "django.template.backends.jinja2.Jinja2", "APP_DIRS": True, "DIRS": []},
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": TEMPLATE_DIRS,
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    },
]
