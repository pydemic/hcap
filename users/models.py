from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import CPFValidator


class User(AbstractUser):
    email = models.EmailField("E-mail", unique=True, help_text="Informe o e-mail.")
    name = models.CharField("Nome completo", max_length=150, help_text="Informe o nome completo.")
    is_verified_notifier = models.BooleanField(
        "Notificador válido?",
        default=False,
        help_text="ATENÇÃO! O usuário terá permissões para notificar alterações de "
        "leitos e utilização hospitalar.",
    )
    is_state_manager = models.BooleanField(
        "Gestor estadual?", default=False, help_text="Marque explicitamente os gestores estaduais."
    )
    cpf = models.CharField(
        "CPF",
        unique=True,
        max_length=14,
        help_text="Informe o CPF no formato xxx.xxx.xxx-xx.",
        validators=[CPFValidator()],
    )
    state = models.ForeignKey(
        "locations.State",
        verbose_name="Estado",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        help_text="É necessário informar o estado.",
    )

    @property
    def first_name(self):
        return (self.name.split() or ("",))[0]

    @property
    def last_name(self):
        return " ".join(self.name.split()[1:])

    @first_name.setter
    def first_name(self, value):
        parts = self.name.split(maxsplit=1) or [""]
        parts[0] = value or ""
        self.name = " ".join(parts)

    @last_name.setter
    def last_name(self, value):
        parts = self.name.split(maxsplit=1) or [""]
        self.name = parts[0] + (value or "")

    @property
    def has_verified_email(self):
        return self.emailaddress_set.filter(verified=True).exists()

    def __str__(self):
        return self.get_full_name()

    def save(self, *args, **kwargs):
        self.clean()
        return super().save(*args, **kwargs)

    def clean(self):
        self.email = self.email.lower()
        self.username = self.username.lower()
        super().clean()
