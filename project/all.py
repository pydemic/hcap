from django.core.exceptions import ImproperlyConfigured

from .run import *

start()

from locations.models import *
from users.models import *
from app.models import *
