from django.apps import AppConfig
from material.frontend.apps import ModuleMixin


class AppConfig(ModuleMixin, AppConfig):
    name = 'app'
    verbose_name = 'Capacidade Hospitalar'
    icon = '<i class="material-icons">settings_applications</i>'
