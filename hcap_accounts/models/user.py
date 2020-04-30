from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from hcap_accounts.managers import UserManager
from hcap_utils.contrib.validations import CPFValidator


class User(AbstractUser):
    username = None
    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = "name", "cpf"

    email = models.EmailField(
        _("email address"), unique=True, help_text=_("Required. Must be a valid email address.")
    )

    name = models.CharField(
        _("full name"), max_length=150, help_text=_("Required. At most 150 characters.")
    )

    cpf = models.CharField(
        _("CPF"),
        max_length=14,
        unique=True,
        help_text=_('Required. 11 digits formatted as "000.000.000-00".'),
        validators=[CPFValidator()],
    )

    class Meta(AbstractUser.Meta):
        ordering = ("name", "email")

    def __init__(self, *args, username=None, email=None, **kwargs):
        if email is None:
            email = email or username
            kwargs["email"] = email
        super().__init__(*args, **kwargs)

    def __str__(self):
        return self.name

    def clean(self):
        self.email = self.email.lower()
        super().clean()

    @property
    def first_name(self):
        return (self.name.split() or ("",))[0]

    @first_name.setter
    def first_name(self, value):
        parts = self.name.split(maxsplit=1) or [""]
        parts[0] = value or ""
        self.name = " ".join(parts)

    @property
    def last_name(self):
        return " ".join(self.name.split()[1:])

    @last_name.setter
    def last_name(self, value):
        parts = self.name.split(maxsplit=1) or [""]
        self.name = parts[0] + (value or "")

    @property
    def has_verified_email(self):
        return self.emailaddress_set.filter(verified=True).exists()

    @property
    def is_manager(self):
        return self.is_active and self.region_managers.filter(is_authorized=True).exists()

    @property
    def is_notifier(self):
        return self.is_active and self.healthcare_unit_notifiers.filter(is_authorized=True).exists()

    @property
    def has_pending_authorization(self):
        return (
            self.region_managers.filter(is_authorized=False).exists()
            or self.healthcare_unit_notifiers.filter(is_authorized=False).exists()
        )
