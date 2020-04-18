"""
django:
    https://docs.djangoproject.com/en/3.0/ref/settings/#secret-key
"""

from hcap.settings.env import env

SECRET_KEY = env("HCAP__SECRET_KEY", default="changeme")
