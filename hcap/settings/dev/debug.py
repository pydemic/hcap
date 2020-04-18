"""
django:
    https://docs.djangoproject.com/en/3.0/ref/settings/#debug
"""

from hcap.settings.env import env

DEBUG = True
CHEAT = env("HCAP__CHEAT", default=False)
