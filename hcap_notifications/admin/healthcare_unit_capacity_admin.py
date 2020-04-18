from django.contrib import admin
from hcap_notifications.models import HealthcareUnitCapacity


@admin.register(HealthcareUnitCapacity)
class HealthcareUnitCapacityAdmin(admin.ModelAdmin):
    list_display = ("healthcare_unit", "notifier", "date")
    search_fields = ("healthcare_unit", "notifier")
