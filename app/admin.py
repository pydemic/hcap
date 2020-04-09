from allauth.account.models import EmailAddress
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from . import models

admin.site.register(models.HealthcareUnity)
admin.site.register(models.Capacity)
admin.site.register(models.LogEntry)


class EmailAddressInline(admin.TabularInline):
    model = EmailAddress
    extra = 0


@admin.register(get_user_model())
class UserAdmin(DjangoUserAdmin):
    list_display = (
        "id",
        "first_name",
        "last_name",
        "email",
        "is_active",
        "is_staff",
        "state",
    )

    list_filter = ("is_active", "is_staff", "state")
    search_fields = ("id", "first_name", "last_name", "email")

    fieldsets = (
        (None, {"fields": ("id",)}),
        ("Informações pessoais", {"fields": ("first_name", "last_name", "email", "cpf")}),
        ("Permissões", {"fields": ("is_active", "is_staff")}),
        ("Atuação", {"fields": ("state",)}),
        ("Datas importantes", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            "Informações pessiais",
            {"fields": ("first_name", "last_name", "email", "cpf", "password1", "password2")},
        ),
        ("Permissões", {"fields": ("is_active", "is_staff")}),
        ("Atuação", {"fields": ("state",)}),
    )

    inlines = (EmailAddressInline,)

    readonly_fields = ("id", "date_joined", "last_login")

    def verified(self, user):
        return user.verified()
