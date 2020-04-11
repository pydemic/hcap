from django.contrib.admin import AdminSite, site

from . import models

site.register(models.HealthcareUnit)
site.register(models.Capacity)
site.register(models.LogEntry)
