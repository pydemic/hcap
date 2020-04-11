"""
django:
    https://docs.djangoproject.com/en/3.0/ref/settings/#databases
"""

from ..env import env
from .paths import SQLITE_PATH


DATABASE_TYPE = env("HCAP__DATABASE_TYPE", default="sqlite")

if DATABASE_TYPE == "sqlite":
    DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": str(SQLITE_PATH)}}
elif DATABASE_TYPE == "postgresql":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": env("HCAP__POSTGRES_DB", default="hcapacity"),
            "USER": env("HCAP__POSTGRES_USER", default="hcapacity"),
            "PASSWORD": env("HCAP__POSTGRES_PASSWORD", default="hcapacity"),
            "HOST": env("HCAP__POSTGRES_HOST", default="postgres"),
            "PORT": env("HCAP__POSTGRES_PORT", default=5432),
        }
    }
