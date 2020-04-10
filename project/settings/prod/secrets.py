"""
django:
    https://docs.djangoproject.com/en/3.0/ref/settings/#secret-key
"""

from project.settings import env

SECRET_KEY = env("HC__SECRET_KEY", default="changeme")
