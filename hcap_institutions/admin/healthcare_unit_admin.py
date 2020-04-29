from django.contrib import admin
from hcap_geo.models import Region
from hcap_institutions.models import HealthcareUnit
from django.utils.translation import gettext_lazy as _


class StateFilter(admin.RelatedFieldListFilter):
    def field_choices(self, field, request, model_admin):
        return field.get_choices(include_blank=False, limit_choices_to={"kind": Region.KIND_STATE})


@admin.register(HealthcareUnit)
class HealthcareUnitAdmin(admin.ModelAdmin):
    list_display = ("cnes_id", "name", "is_active", "city", "state")
    list_filter = ("is_active", ("state", StateFilter))
    search_fields = ("cnes_id", "name")

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "city":
            kwargs["queryset"] = Region.objects.filter(kind=Region.KIND_CITY)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
