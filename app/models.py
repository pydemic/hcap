import datetime
import json
from pathlib import Path

from django.core import validators
from django.db import models
from model_utils.models import TimeStampedModel

from app.fields import HospitalBedsField


class State(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=3)

    class Meta:
        verbose_name = 'Estado'
        verbose_name_plural = 'Estados'
        permissions = [('fill', 'Pode adicionar lista de estados no banco')]

    @classmethod
    def fill_states(cls):
        with open(Path(__file__).parent / 'states.json') as fd:
            data = json.load(fd)
        return [cls.objects.update_or_create(**st)[0] for st in data]

    def __str__(self):
        return self.name


class Municipality(models.Model):
    id = models.IntegerField(primary_key=True)
    state = models.ForeignKey(
        'State',
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Município'
        verbose_name_plural = 'Municípios'

    @classmethod
    def fill_municipality(cls):
        with open(Path(__file__).parent / 'cities.json') as fd:
            data = json.load(fd)

        def fix(d):
            del d['state_code']
            return d

        return [cls.objects.update_or_create(**fix(st))[0] for st in data]

    def __str__(self):
        return self.name


class HealthcareUnity(models.Model):
    municipality = models.ForeignKey(
        'Municipality',
        on_delete=models.CASCADE,
    )
    is_validated = models.BooleanField(
        'Unidade foi validada por um gestor?',
        default=False,
    )
    cnes_id = models.CharField(
        'Registro CNES',
        max_length=15,
        validators=[validators.RegexValidator(r'[0-9]+')],
    )
    name = models.CharField(
        'Estabelecimento',
        max_length=100,
        help_text='Nome do estabelecimento de saúde'
    )
    contact = models.CharField(
        'Nome do profissional',
        max_length=150,
        help_text='Nome completo do profissional responsável pelo cadastro',
    )
    phone = models.CharField(
        'Telefone',
        max_length=150,
        validators=[validators.RegexValidator(
            r'\(\d{2}\)\s?\d{4,5}-?\d{4}',
            'Não esqueça dos parênteses e hífens no número de telefone',
        )],
        help_text='Utilize o formato (XX) XXXXX-XXXX',
    )
    email = models.EmailField(
        'E-mail',
        max_length=150,
    )

    class Meta:
        verbose_name = 'Estabelecimento de Saúde'
        verbose_name_plural = 'Estabelecimentos de Saúde'

    def __str__(self):
        return self.name


class Capacity(TimeStampedModel):
    unity = models.ForeignKey(
        'HealthcareUnity',
        on_delete=models.CASCADE,
    )
    beds_adults = HospitalBedsField(
        "Leitos clínicos de adultos",
        help_text="Informe a capacidade total.",
    )
    beds_pediatric = HospitalBedsField(
        "Leitos clínicos pediátricos",
        help_text="Informe a capacidade total.",
    )
    icu_adults = HospitalBedsField(
        "Leitos UTI adulto",
        help_text="Informe a capacidade total.",
    )
    icu_pediatric = HospitalBedsField(
        "Leitos UTI pediátrico",
        help_text="Informe a capacidade total.",
    )
    created_date = property(lambda self: to_date(self.created))

    class Meta:
        verbose_name = 'Capacidade'
        verbose_name_plural = 'Valores de capacidade'

    def __str__(self):
        return f'{self.unity} ({self.created_date})'


class LogEntry(TimeStampedModel):
    unity = models.ForeignKey(
        'HealthcareUnity',
        on_delete=models.CASCADE
    )
    date = models.DateField()

    # SARI - adults
    sari_beds_adults = HospitalBedsField(
        "Ocupação de leitos clínicos de adultos por SRAG",
        help_text="Informe quantos leitos deste tipo estão ocupados apenas por Síndrome "
                  "Respiratória Aguda Grave",
    )
    covid_cases_adults = HospitalBedsField(
        "Casos COVID confirmados",
        help_text="Informe quantos casos de COVID dentro dessa categoria.",
    )

    # SARI - pediatric
    sari_beds_pediatric = HospitalBedsField(
        "Ocupação de leitos clínicos pediátricos por SRAG",
        help_text="Informe quantos leitos deste tipo estão ocupados apenas por Síndrome "
                  "Respiratória Aguda Grave",
    )
    covid_cases_pediatric = HospitalBedsField(
        "Casos COVID confirmados",
        help_text="Informe quantos casos de COVID dentro dessa categoria.",
    )

    # SARI - ICU adults
    sari_icu_adults = HospitalBedsField(
        "Ocupação de leitos UTI adulto por SRAG",
        help_text="Informe quantos leitos deste tipo estão ocupado apenas por Síndrome "
                  "Respiratória Aguda Grave.",
    )
    covid_casesadults = HospitalBedsField(
        "Casos COVID confirmados",
        help_text="Informe quantos casos de COVID dentro dessa categoria.",
    )

    # SARI - ICU pediatric
    sari_icu_pediatric = HospitalBedsField(
        "Ocupação de leitos UTI pediátrico por SRAG",
        help_text="Informe quantos leitos deste tipo estão ocupado apenas por Síndrome "
                  "Respiratória Aguda Grave.",
    )
    covid_casespediatric = HospitalBedsField(
        "Casos COVID confirmados",
        help_text="Informe quantos casos de COVID dentro dessa categoria.",
    )

    # Regular
    regular_beds_adults = HospitalBedsField(
        "Ocupação de leitos clínicos de adultos (outras causas)",
        help_text="Informe quantos leitos deste tipo estão ocupados.",
    )
    regular_beds_pediatric = HospitalBedsField(
        "Ocupação de leitos clínicos pediátricos (outras causas)",
        help_text="Informe quantos leitos deste tipo estão ocupados.",
    )
    regular_icu_adults = HospitalBedsField(
        "Ocupação de leitos UTI adulto (outras causas)",
        help_text="Informe quantos leitos deste tipo estão ocupados.",
    )
    regular_icu_pediatric = HospitalBedsField(
        "Ocupação de leitos UTI pediátrico (outras causas)",
        help_text="Informe quantos leitos deste tipo estão ocupados.",
    )

    class Meta:
        verbose_name = 'Entrada de caso'
        verbose_name_plural = 'Entradas de casos'


def to_date(dt):
    return datetime.date(dt.year, dt.month, dt.day)
