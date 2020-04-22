"""
django:
    https://docs.djangoproject.com/en/3.0/ref/settings/#databases
    https://docs.djangoproject.com/en/3.0/ref/settings/#email-file-path
    https://docs.djangoproject.com/en/3.0/ref/settings/#locale-paths
    https://docs.djangoproject.com/en/3.0/ref/settings/#media-root
    https://docs.djangoproject.com/en/3.0/ref/settings/#static-root
    https://docs.djangoproject.com/en/3.0/ref/settings/#staticfiles-dirs
    https://docs.djangoproject.com/en/3.0/ref/settings/#templates
"""

from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.parent.parent

EMAIL_FILE_PATH = BASE_DIR / "email_messages"
SQLITE_PATH = BASE_DIR / "db.sqlite3"

MEDIA_ROOT = BASE_DIR / "media"
STATIC_ROOT = BASE_DIR / "static"

LOCALE_PATHS = (BASE_DIR / "locale",)

STATICFILES_DIRS = (BASE_DIR / "hcap" / "static",)
TEMPLATE_DIRS = (BASE_DIR / "hcap" / "templates",)
