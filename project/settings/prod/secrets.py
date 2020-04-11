"""
django:
    https://docs.djangoproject.com/en/3.0/ref/settings/#secret-key
"""

from project.settings import env

SECRET_KEY = env("HCAP__SECRET_KEY", default="changeme")
