from django.apps import AppConfig
from material.frontend.apps import ModuleMixin


class AppConfig(ModuleMixin, AppConfig):
    name = "app"
    verbose_name = "Monitoramento de ocupação hospitalar"
    icon = '<i class="material-icons">local_hospital</i>'
