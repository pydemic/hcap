from django.contrib import admin
from hcap_notifications.models import HealthcareUnitCondition


@admin.register(HealthcareUnitCondition)
class HealthcareUnitConditionAdmin(admin.ModelAdmin):
    list_display = ("healthcare_unit", "notifier", "date")
    search_fields = ("healthcare_unit", "notifier")
