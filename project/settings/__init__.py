"""
django:
    https://docs.djangoproject.com/en/3.0/topics/settings/
    https://docs.djangoproject.com/en/3.0/ref/settings
"""

from .env import ENV
from .general import *

if ENV == "dev":
    from .dev import *
elif ENV == "test":
    from .test import *
elif ENV == "prod":
    from .prod import *
