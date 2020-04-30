from django.contrib import admin

from hcap_geo import models


@admin.register(models.Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "abbr", "kind")

    list_filter = ("kind",)

    search_fields = ("code", "name", "abbr")
