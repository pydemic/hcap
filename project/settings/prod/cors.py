"""
django:
    https://docs.djangoproject.com/en/3.0/ref/settings/#allowed-hosts
"""

from ..env import env

ALLOWED_HOSTS = env("HC__ALLOWED_HOSTS", default=[])
