from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import CPFValidator


class User(AbstractUser):
    email = models.EmailField("E-mail", unique=True, help_text="Informe o e-mail.")
    first_name = models.CharField("Nome", max_length=100, help_text="Informe o nome.")
    last_name = models.CharField("Sobrenome", max_length=100, help_text="Informe o sobrenome.")
    is_verified_notifier = models.BooleanField(
        "Notificador válido?",
        default=None,
        help_text="ATENÇÃO! O usuário terá permissões para notificar alterações de leitos e utilização hospitalar.",
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