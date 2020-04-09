import datetime

from django.core import validators
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.timezone import now
from model_utils.models import TimeStampedModel

from app.fields import HospitalBedsField


class HealthcareUnity(models.Model):
    municipality = models.ForeignKey(
        "locations.Municipality",
        on_delete=models.CASCADE,
        related_name='healthcare_unities',
        verbose_name="Município",
    )
    cnes_id = models.CharField(
        "Registro CNES",
        max_length=15,
        validators=[validators.RegexValidator(r"[0-9]+")],
    )
    is_active = models.BooleanField(
        "Unidade está ativa?",
        default=True,
    )
    name = models.CharField(
        "Estabelecimento", max_length=100, help_text="Nome do estabelecimento de saúde"
    )
    notifiers = models.ManyToManyField('auth.User', related_name='unities')

    class Meta:
        verbose_name = "Estabelecimento de Saúde"
        verbose_name_plural = "Estabelecimentos de Saúde"

    def __str__(self):
        return self.name


class Capacity(TimeStampedModel):
    unity = models.ForeignKey("HealthcareUnity", on_delete=models.CASCADE, )
    date = models.DateField(
        "Data",
        help_text="Quando ocorreu a alteração na capacidade hospitalar?",
        default=now,
    )
    beds_adults = HospitalBedsField(
        "Adulto", help_text="Quantos leitos deste tipo você tem?",
    )
    beds_pediatric = HospitalBedsField(
        "Pediátrico", help_text="Quantos leitos deste tipo você tem?",
    )
    icu_adults = HospitalBedsField(
        "Adulto", help_text="Quantos leitos deste tipo você tem?",
    )
    icu_pediatric = HospitalBedsField(
        "Pediátrico", help_text="Quantos leitos deste tipo você tem?",
    )
    created_date = property(lambda self: to_date(self.created))

    class Meta:
        verbose_name = "Alteração na capacidade"
        verbose_name_plural = "Alterações de capacidade hospitalar"

    def __str__(self):
        return f"{self.unity} ({self.created_date})"


class LogEntry(TimeStampedModel):
    unity = models.ForeignKey("HealthcareUnity", on_delete=models.CASCADE)
    date = models.DateField(
        "Data",
        help_text="De quando é este dado?",
        default=now,
    )

    # SARI - adults
    sari_cases_adults = HospitalBedsField(
        "Adulto",
        help_text="Informe total de pacientes SRAG",
    )
    covid_cases_adults = HospitalBedsField(
        "Casos COVID confirmados",
        blank=True,
        help_text="Destes casos, quantos foram confirmados como COVID?",
    )

    # SARI - pediatric
    sari_cases_pediatric = HospitalBedsField(
        "Pediátrico",
        help_text="Informe total de pacientes SRAG",
    )
    covid_cases_pediatric = HospitalBedsField(
        "Casos COVID confirmados",
        blank=True,
        help_text="Destes casos, quantos foram confirmados como COVID?",
    )

    # SARI - ICU adults
    icu_sari_cases_adults = HospitalBedsField(
        "Adulto",
        help_text="Informe total de pacientes SRAG",
    )
    icu_covid_cases_adults = HospitalBedsField(
        "Casos COVID confirmados",
        blank=True,
        help_text="Destes casos, quantos foram confirmados como COVID?",
    )

    # SARI - ICU pediatric
    icu_sari_cases_pediatric = HospitalBedsField(
        "Pediátrico",
        help_text="Informe total de pacientes para SRAG",
    )
    icu_covid_cases_pediatric = HospitalBedsField(
        "Casos COVID confirmados",
        blank=True,
        help_text="Destes casos, quantos foram confirmados como COVID?",
    )

    # Regular
    regular_cases_adults = HospitalBedsField(
        "Adulto",
        help_text="Informe o total de pacientes.",
    )
    regular_cases_pediatric = HospitalBedsField(
        "Pediátrico",
        help_text="Informe o total de pacientes.",
    )
    regular_icu_adults = HospitalBedsField(
        "Adulto",
        help_text="Informe o total de pacientes.",
    )
    regular_icu_pediatric = HospitalBedsField(
        "Pediátrico",
        help_text="Informe o total de pacientes.",
    )

    class Meta:
        verbose_name = "Informe diário"
        verbose_name_plural = "Informes diários"

    def __str__(self):
        return f"{self.unity} - {self.date.strftime('%x')}"

    def clean_fields(self, exclude=None):
        if 'covid_cases_adults' not in exclude:
            self.covid_cases_adults = self.covid_cases_adults or 0
        if 'covid_cases_pediatric' not in exclude:
            self.covid_cases_pediatric = self.covid_cases_pediatric or 0
        if 'icu_covid_cases_adults' not in exclude:
            self.icu_covid_cases_adults = self.icu_covid_cases_adults or 0
        if 'icu_covid_cases_pediatric' not in exclude:
            self.icu_covid_cases_pediatric = self.icu_covid_cases_pediatric or 0
        return super().clean_fields(exclude=exclude)

    def clean(self):
        errors = {}
        msg = "Número de casos COVID não pode ser maior que o SRAG."
        if self.covid_cases_adults > self.sari_cases_adults:
            errors['covid_cases_adults'] = msg
        if self.covid_cases_pediatric > self.sari_cases_pediatric:
            errors['covid_cases_pediatric'] = msg
        if self.icu_covid_cases_adults > self.icu_sari_cases_adults:
            errors['icu_covid_cases_adults'] = msg
        if self.icu_covid_cases_pediatric > self.icu_sari_cases_pediatric:
            errors['icu_covid_cases_pediatric'] = msg
        if errors:
            raise ValidationError(errors)


def to_date(dt):
    return datetime.date(dt.year, dt.month, dt.day)
