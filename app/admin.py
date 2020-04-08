from django.contrib import admin

from . import models

admin.site.register(models.HealthcareUnity)
admin.site.register(models.Capacity)
admin.site.register(models.LogEntry)
