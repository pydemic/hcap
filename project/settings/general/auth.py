"""
django:
    https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators
    https://docs.djangoproject.com/en/3.0/topics/auth/customizing/#substituting-a-custom-user-model
django-allauth:
    https://django-allauth.readthedocs.io/en/latest/installation.html
    https://django-allauth.readthedocs.io/en/latest/configuration.html
"""

AUTH_USER_MODEL = "users.User"

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)

# Allauth

ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_USER_MODEL_USERNAME_FIELD = "email"
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
LOGIN_REDIRECT_URL = "/"
SOCIALACCOUNT_QUERY_EMAIL = True
ACCOUNT_USERNAME_BLACKLIST = [
    "administrator",
    "help",
    "helpdesk",
    "operator",
    "root",
    "superadmin",
    "superuser",
    "info",
    "admin",
    "webmaster",
    "areariservata",
    "blog",
    "master",
]
ACCOUNT_ADAPTER = "app.adapters.AccountAdapter"
ACCOUNT_FORMS = {"signup": "app.forms.SignupForm"}
