from django.apps import AppConfig as DjangoAppConfig
from django.utils.translation import gettext_lazy as _
from material.frontend.apps import ModuleMixin


class AppConfig(ModuleMixin, DjangoAppConfig):
    name = "hcap"
    verbose_name = _("Hospital Capacity")
    icon = '<i class="material-icons">local_hospital</i>'
