from django.contrib.admin import AdminSite, site, ModelAdmin, register

from . import models
from .filters import custom_titled_filter

# site.register(models.HealthcareUnit)
site.register(models.Capacity)
# site.register(models.LogEntry)


@register(models.HealthcareUnit)
class HealthcareUnitAdmin(ModelAdmin):
    search_fields = ["cnes_id", "name"]
    list_display = ("cnes_id", "name", "get_city_name", "is_active")
    list_filter = ("is_active", ("city__state__name", custom_titled_filter("Estado")))

    def get_city_name(self, healthcare_unit):
        return healthcare_unit.city.name

    get_city_name.short_description = "Município"
    get_city_name.admin_order_field = "city__name"

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("city")


@register(models.LogEntry)
class LogEntryAdmin(ModelAdmin):
    search_fields = ["unit__cnes_id", "unit__name"]
    list_display = ("get_cnes_id", "get_unit_name", "get_date")

    def get_cnes_id(self, log_entry):
        return log_entry.unit.cnes_id

    def get_unit_name(self, log_entry):
        return log_entry.unit.name

    def get_date(self, log_entry):
        return log_entry.date.strftime("%x")

    get_cnes_id.short_description = "CNES"
    get_cnes_id.admin_order_field = "unit__cnes_id"
    get_unit_name.short_description = "Nome do Estabelecimento"
    get_unit_name.admin_order_field = "unit__name"
    get_date.short_description = "Data da Entrada"
    get_date.admin_order_field = "date"
