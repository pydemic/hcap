import datetime

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core import validators
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.timezone import now
from model_utils.models import TimeStampedModel

from .fields import HospitalBedsField
from .managers import HealthcareUnitManager, CapacityManager, LogEntryManager


class HealthcareUnit(models.Model):
    city = models.ForeignKey(
        "locations.City",
        on_delete=models.CASCADE,
        related_name="healthcare_units",
        verbose_name="Município",
    )
    cnes_id = models.CharField(
        "Registro CNES",
        max_length=15,
        validators=[validators.RegexValidator(r"[0-9]+")],
        db_index=True,
    )
    is_active = models.BooleanField("Unidade está ativa?", default=True)
    name = models.CharField(
        "Estabelecimento", max_length=100, help_text="Nome do estabelecimento de saúde"
    )
    objects = HealthcareUnitManager()

    @property
    def notifiers(self):
        return NotifierForHealthcareUnit.objects.filter(unit=self, is_approved=True)

    class Meta:
        verbose_name = "Estabelecimento de Saúde"
        verbose_name_plural = "Estabelecimentos de Saúde"

    def __str__(self):
        return self.name

    def register_notifier(self, user, authorize=True):
        """
        Register user as a valid notifier.

        If authorize = False, create association, but dis-authorize user.
        """
        user.is_authorized = authorize
        user.role = user.ROLE_NOTIFIER
        user.save()
        if authorize:
            authorize_notifier(user, self)
        else:
            associate_notifier(user, self)


class Capacity(TimeStampedModel):
    unit = models.ForeignKey(
        "HealthcareUnit",
        on_delete=models.CASCADE,
        verbose_name="Unidade de saúde",
        related_name="capacity_notifications",
    )
    notifier = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Usuário notificador",
        related_name="capacity_notifications",
    )
    date = models.DateField(
        "Data",
        default=now,
        help_text="Quando ocorreu a alteração na capacidade hospitalar?",
        db_index=True,
    )
    beds_adults = HospitalBedsField("Adulto", help_text="Quantos leitos deste tipo você tem?")
    beds_pediatric = HospitalBedsField(
        "Pediátrico", help_text="Quantos leitos deste tipo você tem?"
    )
    icu_adults = HospitalBedsField("Adulto", help_text="Quantos leitos deste tipo você tem?")
    icu_pediatric = HospitalBedsField("Pediátrico", help_text="Quantos leitos deste tipo você tem?")
    created_date = property(lambda self: to_date(self.created))
    objects = CapacityManager()

    @property
    def capacities(self):
        return dict(
            beds_adults=self.beds_adults,
            beds_pediatric=self.beds_pediatric,
            icu_adults=self.icu_adults,
            icu_pediatric=self.icu_pediatric,
        )

    @property
    def capacities_tuple(self):
        return (self.beds_adults, self.beds_pediatric, self.icu_adults, self.icu_pediatric)

    @property
    def icu_and_beds_total(self):
        return self.beds_adults + self.beds_pediatric + self.icu_adults + self.icu_pediatric

    @property
    def icu_total(self):
        return self.icu_adults + self.icu_pediatric

    @property
    def beds_total(self):
        return self.beds_adults + self.beds_pediatric

    class Meta:
        verbose_name = "Alteração na capacidade"
        verbose_name_plural = "Alterações de capacidade hospitalar"

    def __str__(self):
        return f"{self.unit} ({self.date})"


class LogEntry(TimeStampedModel):
    unit = models.ForeignKey(
        "HealthcareUnit",
        on_delete=models.CASCADE,
        verbose_name="Estabelecimento de Saúde",
        related_name="notifications",
    )
    notifier = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Usuário notificador",
        related_name="daily_notifications",
    )
    date = models.DateField("Data", help_text="De quando é este dado?", default=now, db_index=True)

    # SARI - adults
    sari_cases_adults = HospitalBedsField("Adulto", help_text="Informe total de pacientes SRAG")
    covid_cases_adults = HospitalBedsField(
        "Casos COVID confirmados",
        blank=True,
        help_text="Destes casos, quantos foram confirmados como COVID?",
    )

    # SARI - pediatric
    sari_cases_pediatric = HospitalBedsField(
        "Pediátrico", help_text="Informe total de pacientes SRAG"
    )
    covid_cases_pediatric = HospitalBedsField(
        "Casos COVID confirmados",
        blank=True,
        help_text="Destes casos, quantos foram confirmados como COVID?",
    )

    # SARI - ICU adults
    icu_sari_cases_adults = HospitalBedsField("Adulto", help_text="Informe total de pacientes SRAG")
    icu_covid_cases_adults = HospitalBedsField(
        "Casos COVID confirmados",
        blank=True,
        help_text="Destes casos, quantos foram confirmados como COVID?",
    )

    # SARI - ICU pediatric
    icu_sari_cases_pediatric = HospitalBedsField(
        "Pediátrico", help_text="Informe total de pacientes para SRAG"
    )
    icu_covid_cases_pediatric = HospitalBedsField(
        "Casos COVID confirmados",
        blank=True,
        help_text="Destes casos, quantos foram confirmados como COVID?",
    )

    # Regular
    regular_cases_adults = HospitalBedsField("Adulto", help_text="Informe o total de pacientes.")
    regular_cases_pediatric = HospitalBedsField(
        "Pediátrico", help_text="Informe o total de pacientes."
    )
    icu_regular_adults = HospitalBedsField("Adulto", help_text="Informe o total de pacientes.")
    icu_regular_pediatric = HospitalBedsField(
        "Pediátrico", help_text="Informe o total de pacientes."
    )

    @property
    def cases(self):
        return {
            "sari_cases_adults": self.sari_cases_adults,
            "covid_cases_adults": self.covid_cases_adults,
            "sari_cases_pediatric": self.sari_cases_pediatric,
            "covid_cases_pediatric": self.covid_cases_pediatric,
            "icu_sari_cases_adults": self.icu_sari_cases_adults,
            "icu_covid_cases_adults": self.icu_covid_cases_adults,
            "icu_sari_cases_pediatric": self.icu_sari_cases_pediatric,
            "icu_covid_cases_pediatric": self.icu_covid_cases_pediatric,
            "regular_cases_adults": self.regular_cases_adults,
            "regular_cases_pediatric": self.regular_cases_pediatric,
            "icu_regular_adults": self.icu_regular_adults,
            "icu_regular_pediatric": self.icu_regular_pediatric,
        }

    @property
    def cases_tuple(self):
        return tuple(self.cases.values())

    @property
    def icu_and_cases_total(self):
        return self.icu_total + self.cases_total

    @property
    def icu_total(self):
        return (
            self.icu_sari_cases_adults
            + self.icu_sari_cases_pediatric
            + self.icu_regular_adults
            + self.icu_regular_pediatric
        )

    @property
    def cases_total(self):
        return (
            self.sari_cases_adults
            + self.sari_cases_pediatric
            + self.regular_cases_adults
            + self.regular_cases_pediatric
        )

    @property
    def covid_total(self):
        return (
            self.covid_cases_adults
            + self.covid_cases_pediatric
            + self.icu_covid_cases_adults
            + self.icu_covid_cases_pediatric
        )

    objects = LogEntryManager()

    class Meta:
        verbose_name = "Informe diário"
        verbose_name_plural = "Informes diários"

    def __str__(self):
        return f"{self.unit} - {self.date.strftime('%x')}"

    def clean_fields(self, exclude=None):
        if "covid_cases_adults" not in exclude:
            self.covid_cases_adults = self.covid_cases_adults or 0
        if "covid_cases_pediatric" not in exclude:
            self.covid_cases_pediatric = self.covid_cases_pediatric or 0
        if "icu_covid_cases_adults" not in exclude:
            self.icu_covid_cases_adults = self.icu_covid_cases_adults or 0
        if "icu_covid_cases_pediatric" not in exclude:
            self.icu_covid_cases_pediatric = self.icu_covid_cases_pediatric or 0
        return super().clean_fields(exclude=exclude)

    def clean(self):
        errors = {}
        msg = "Número de casos COVID não pode ser maior que o SRAG."
        if self.covid_cases_adults > self.sari_cases_adults:
            errors["covid_cases_adults"] = msg
        if self.covid_cases_pediatric > self.sari_cases_pediatric:
            errors["covid_cases_pediatric"] = msg
        if self.icu_covid_cases_adults > self.icu_sari_cases_adults:
            errors["icu_covid_cases_adults"] = msg
        if self.icu_covid_cases_pediatric > self.icu_sari_cases_pediatric:
            errors["icu_covid_cases_pediatric"] = msg
        if errors:
            raise ValidationError(errors)


class NotifierForHealthcareUnit(models.Model):
    notifier = models.ForeignKey(
        settings.AUTH_USER_MODEL, models.CASCADE, verbose_name="Notificador"
    )
    unit = models.ForeignKey(
        HealthcareUnit, models.CASCADE, verbose_name="Estabelecimento de Saúde"
    )
    is_approved = models.BooleanField("Aprovado", default=False)

    def __str__(self):
        return f"{self.notifier} de {self.unit}"

    class Meta:
        verbose_name = "Notificador de Estabelecimento de Saúde"
        verbose_name_plural = "Notificadores de Estabelecimento de Saúde"
        unique_together = [("notifier", "unit")]


def authorize_notifier(user, unit):
    NotifierForHealthcareUnit.objects.update_or_create(notifier=user, unit=unit, is_approved=True)


def associate_notifier(user, unit):
    NotifierForHealthcareUnit.objects.update_or_create(notifier=user, unit=unit, is_approved=False)


def to_date(dt):
    return datetime.date(dt.year, dt.month, dt.day)


#
# Modify user to have the healthcare_units property
#
@property
def healthcare_units(user):
    m2m = NotifierForHealthcareUnit.objects
    pks = m2m.filter(notifier=user, is_approved=True).values_list("notifier_id", flat=True)
    pks = list(pks)
    if len(pks) == 1:
        return HealthcareUnit.objects.filter(pk=pks[0])
    else:
        return HealthcareUnit.objects.filter(pk__in=pks)


get_user_model().healthcare_units = healthcare_units
