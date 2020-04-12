from django.contrib.admin import AdminSite, site, ModelAdmin, register

from . import models
from .filters import custom_titled_filter

# site.register(models.HealthcareUnit)
site.register(models.Capacity)
site.register(models.LogEntry)


@register(models.HealthcareUnit)
class HealthcareUnitAdmin(ModelAdmin):
    search_fields = ["cnes_id", "name"]
    list_display = ("cnes_id", "name", "get_municipality_name", "is_active")
    list_filter = ("is_active", ("municipality__state__name", custom_titled_filter("Estado")))

    def get_municipality_name(self, healthcare_unit):
        return healthcare_unit.municipality.name

    get_municipality_name.short_description = "Município"
    get_municipality_name.admin_order_field = "municipality__name"
