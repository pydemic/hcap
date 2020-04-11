from allauth.account.models import EmailAddress
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin


class EmailAddressInline(admin.TabularInline):
    model = EmailAddress
    extra = 0


class HasVerifiedEmailFilter(admin.SimpleListFilter):
    title = "Email verificado"
    parameter_name = "has_verified_email"

    def lookups(self, request, model_admin):
        return (("Yes", "Sim"), ("No", "Não"))

    def queryset(self, request, queryset):
        value = self.value()
        if value == "Yes":
            return queryset.filter(emailaddress__verified=True)
        if value == "No":
            return queryset.filter(emailaddress__verified=False)
        return queryset


@admin.register(get_user_model())
class UserAdmin(DjangoUserAdmin):
    list_display = ("id", "name", "email", "is_active", "is_staff", "has_verified_email", "state")
    ordering = ("name", "email")
    list_filter = ("is_active", "is_staff", HasVerifiedEmailFilter, "state")
    search_fields = ("id", "name", "email")

    fieldsets = (
        (None, {"fields": ("id",)}),
        ("Informações pessoais", {"fields": ("name", "email", "cpf")}),
        ("Atuação", {"fields": ("role", "state",)}),
        ("Permissões", {"fields": ("is_active", "is_staff", "is_authorized")},),
        ("Datas importantes", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        ("Informações pessoais", {"fields": ("name", "email", "cpf", "password1", "password2")}),
        ("Permissões", {"fields": ("is_active", "is_staff")}),
        ("Atuação", {"fields": ("state",)}),
    )

    inlines = (EmailAddressInline,)

    readonly_fields = ("id", "date_joined", "last_login")

    def has_verified_email(self, user):
        return user.has_verified_email

    has_verified_email.boolean = True
    has_verified_email.short_description = "Email verificado"
