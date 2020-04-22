"""
django:
    https://docs.djangoproject.com/en/3.0/topics/auth/customizing/#substituting-a-custom-user-model
    https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators
    https://docs.djangoproject.com/en/3.0/ref/settings/#authentication-backends
    https://docs.djangoproject.com/en/3.0/ref/settings/#login-redirect-url
django-allauth:
    https://django-allauth.readthedocs.io/en/latest/installation.html
    https://django-allauth.readthedocs.io/en/latest/configuration.html
"""

AUTH_USER_MODEL = "hcap_accounts.User"

AUTH_PASSWORD_VALIDATORS = (
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
)

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)

LOGIN_REDIRECT_URL = "/"

# Allauth

ACCOUNT_ADAPTER = "hcap_utils.contrib.allauth.AccountAdapter"
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_FORMS = {
    "change_password": "hcap_utils.contrib.allauth.ChangePasswordForm",
    "login": "hcap_utils.contrib.allauth.LoginForm",
    "reset_password": "hcap_utils.contrib.allauth.ResetPasswordForm",
    "signup": "hcap_utils.contrib.allauth.SignupForm",
}
ACCOUNT_USER_DISPLAY = "hcap_utils.contrib.allauth.user_display"
ACCOUNT_USER_MODEL_USERNAME_FIELD = "email"
ACCOUNT_USERNAME_REQUIRED = False
