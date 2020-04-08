from django.contrib import admin

from . import models

admin.site.register(models.HealthcareUnity)
admin.site.register(models.Capacity)
admin.site.register(models.LogEntry)


@admin.register(models.State)
class StateAdmin(admin.ModelAdmin):
    actions = ['fill_states']

    def fill_states(self, request, queryset):
        models.State.fill_states()

    fill_states.short_description = "Preenche com a lista de estados"
    fill_states.allowed_permissions = ('add',)


@admin.register(models.Municipality)
class MunicipalityAdmin(admin.ModelAdmin):
    actions = ['fill_cities']

    def fill_cities(self, request, queryset):
        models.Municipality.fill_municipality()

    fill_cities.short_description = "Preenche com a lista de municípios"
    fill_cities.allowed_permissions = ('add',)


