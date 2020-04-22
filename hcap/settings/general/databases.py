"""
django:
    https://docs.djangoproject.com/en/3.0/ref/settings/#databases
"""

from hcap.settings.env import env


DATABASE_TYPE = env("DATABASE_TYPE", default="sqlite")

if DATABASE_TYPE == "sqlite":
    from .paths import SQLITE_PATH

    DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": str(SQLITE_PATH)}}
elif DATABASE_TYPE == "postgresql":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": env("POSTGRES_DB", default="hcap"),
            "USER": env("POSTGRES_USER", default="pydemic"),
            "PASSWORD": env("POSTGRES_PASSWORD", default="pydemic"),
            "HOST": env("POSTGRES_HOST", default="postgres"),
            "PORT": env("POSTGRES_PORT", default=5432),
        }
    }
