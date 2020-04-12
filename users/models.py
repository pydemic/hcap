from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Manager

from .managers import UserManager
from .validators import CPFValidator


class User(AbstractUser):
    ROLE_NONE, ROLE_NOTIFIER, ROLE_MANAGER = range(3)
    ROLE_CHOICES = [
        (ROLE_NONE, "Nenhum"),
        (ROLE_NOTIFIER, "Notificador"),
        (ROLE_MANAGER, "Gestor local"),
    ]

    email = models.EmailField("E-mail", unique=True, help_text="Informe o e-mail.")
    name = models.CharField("Nome completo", max_length=150, help_text="Informe o nome completo.")
    role = models.PositiveSmallIntegerField(
        "Papel do usuário",
        choices=ROLE_CHOICES,
        default=ROLE_NONE,
        help_text="O usuário é notificador ou gestor?",
    )
    is_authorized = models.BooleanField(
        "Autorizado?",
        default=False,
        help_text="Marque para usuários autorizados a operar dentro do seu papel.",
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
        default=53,  # Distrito Federal
        related_name="users",
        on_delete=models.CASCADE,
        help_text="É necessário informar o estado.",
    )
    username = None
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = "name", "cpf"
    objects = UserManager()

    emailaddress_set: Manager

    class Meta(AbstractUser.Meta):
        ordering = ("name", "email")

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

    is_notifier = property(lambda self: self.is_authorized and self.role == self.ROLE_NOTIFIER)
    is_manager = property(lambda self: self.is_authorized and self.role == self.ROLE_MANAGER)

    def __init__(self, *args, username=None, email=None, **kwargs):
        email = email or username
        kwargs["email"] = email
        super().__init__(*args, **kwargs)

    def __str__(self):
        return self.get_full_name()

    def save(self, *args, **kwargs):
        self.clean()
        return super().save(*args, **kwargs)

    def clean(self):
        self.email = self.email.lower()
        super().clean()

    def get_full_name(self):
        return self.name
