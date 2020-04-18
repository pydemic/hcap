from allauth.account.models import EmailAddress
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext_lazy as _

from hcap_accounts.models import HealthcareUnitNotifier, RegionManager


class HasVerifiedEmailFilter(admin.SimpleListFilter):
    title = _("email verified")
    parameter_name = "has_verified_email"

    def lookups(self, request, model_admin):
        return (("Yes", _("Yes")), ("No", _("No")))

    def queryset(self, request, queryset):
        value = self.value()
        if value == "Yes":
            return queryset.filter(emailaddress__verified=True)
        if value == "No":
            return queryset.filter(emailaddress__verified=False)
        return queryset


class EmailAddressInline(admin.TabularInline):
    model = EmailAddress
    extra = 0


class HealthcareUnitNotifierInline(admin.TabularInline):
    model = HealthcareUnitNotifier
    extra = 0


class RegionManagerInline(admin.TabularInline):
    model = RegionManager
    extra = 0


@admin.register(get_user_model())
class UserAdmin(DjangoUserAdmin):
    list_display = ("id", "name", "email", "is_active", "is_staff", "has_verified_email")

    list_filter = ("is_active", "is_staff", HasVerifiedEmailFilter)

    search_fields = ("id", "name", "email")

    ordering = ("name", "email")

    fieldsets = (
        (None, {"fields": ("id",)}),
        (_("Personal info"), {"fields": ("name", "email", "cpf")}),
        (_("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser")}),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (_("Personal info"), {"fields": ("name", "email", "cpf", "password1", "password2")}),
        (_("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser")}),
    )

    inlines = (HealthcareUnitNotifierInline, RegionManagerInline, EmailAddressInline)

    readonly_fields = ("id", "date_joined", "last_login")

    def has_verified_email(self, user):
        return user.has_verified_email

    has_verified_email.boolean = True
    has_verified_email.short_description = _("email verified")
