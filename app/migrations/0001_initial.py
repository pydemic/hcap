# Generated by Django 3.0.5 on 2020-04-08 12:44

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("locations", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="HealthcareUnity",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "is_validated",
                    models.BooleanField(
                        default=False,
                        verbose_name="Unidade foi validada por um gestor?",
                    ),
                ),
                (
                    "cnes_id",
                    models.CharField(
                        max_length=15,
                        validators=[django.core.validators.RegexValidator("[0-9]+")],
                        verbose_name="Registro CNES",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="Nome do estabelecimento de saúde",
                        max_length=100,
                        verbose_name="Estabelecimento",
                    ),
                ),
                (
                    "contact",
                    models.CharField(
                        help_text="Nome completo do profissional responsável pelo cadastro",
                        max_length=150,
                        verbose_name="Nome do profissional",
                    ),
                ),
                (
                    "phone",
                    models.CharField(
                        help_text="Utilize o formato (XX) XXXXX-XXXX",
                        max_length=150,
                        validators=[
                            django.core.validators.RegexValidator(
                                "\\(\\d{2}\\)\\s?\\d{4,5}-?\\d{4}",
                                "Não esqueça dos parênteses e hífens no número de telefone",
                            )
                        ],
                        verbose_name="Telefone",
                    ),
                ),
                ("email", models.EmailField(max_length=150, verbose_name="E-mail")),
                (
                    "municipality",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="locations.Municipality",
                    ),
                ),
            ],
            options={
                "verbose_name": "Estabelecimento de Saúde",
                "verbose_name_plural": "Estabelecimentos de Saúde",
            },
        ),
        migrations.CreateModel(
            name="LogEntry",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    model_utils.fields.AutoCreatedField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name="created",
                    ),
                ),
                (
                    "modified",
                    model_utils.fields.AutoLastModifiedField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name="modified",
                    ),
                ),
                ("date", models.DateField()),
                (
                    "sari_beds_adults",
                    models.PositiveSmallIntegerField(
                        help_text="Informe quantos leitos deste tipo estão ocupados apenas por Síndrome Respiratória Aguda Grave",
                        verbose_name="Ocupação de leitos clínicos de adultos por SRAG",
                    ),
                ),
                (
                    "covid_cases_adults",
                    models.PositiveSmallIntegerField(
                        help_text="Informe quantos casos de COVID dentro dessa categoria.",
                        verbose_name="Casos COVID confirmados",
                    ),
                ),
                (
                    "sari_beds_pediatric",
                    models.PositiveSmallIntegerField(
                        help_text="Informe quantos leitos deste tipo estão ocupados apenas por Síndrome Respiratória Aguda Grave",
                        verbose_name="Ocupação de leitos clínicos pediátricos por SRAG",
                    ),
                ),
                (
                    "covid_cases_pediatric",
                    models.PositiveSmallIntegerField(
                        help_text="Informe quantos casos de COVID dentro dessa categoria.",
                        verbose_name="Casos COVID confirmados",
                    ),
                ),
                (
                    "sari_icu_adults",
                    models.PositiveSmallIntegerField(
                        help_text="Informe quantos leitos deste tipo estão ocupado apenas por Síndrome Respiratória Aguda Grave.",
                        verbose_name="Ocupação de leitos UTI adulto por SRAG",
                    ),
                ),
                (
                    "covid_casesadults",
                    models.PositiveSmallIntegerField(
                        help_text="Informe quantos casos de COVID dentro dessa categoria.",
                        verbose_name="Casos COVID confirmados",
                    ),
                ),
                (
                    "sari_icu_pediatric",
                    models.PositiveSmallIntegerField(
                        help_text="Informe quantos leitos deste tipo estão ocupado apenas por Síndrome Respiratória Aguda Grave.",
                        verbose_name="Ocupação de leitos UTI pediátrico por SRAG",
                    ),
                ),
                (
                    "covid_casespediatric",
                    models.PositiveSmallIntegerField(
                        help_text="Informe quantos casos de COVID dentro dessa categoria.",
                        verbose_name="Casos COVID confirmados",
                    ),
                ),
                (
                    "regular_beds_adults",
                    models.PositiveSmallIntegerField(
                        help_text="Informe quantos leitos deste tipo estão ocupados.",
                        verbose_name="Ocupação de leitos clínicos de adultos (outras causas)",
                    ),
                ),
                (
                    "regular_beds_pediatric",
                    models.PositiveSmallIntegerField(
                        help_text="Informe quantos leitos deste tipo estão ocupados.",
                        verbose_name="Ocupação de leitos clínicos pediátricos (outras causas)",
                    ),
                ),
                (
                    "regular_icu_adults",
                    models.PositiveSmallIntegerField(
                        help_text="Informe quantos leitos deste tipo estão ocupados.",
                        verbose_name="Ocupação de leitos UTI adulto (outras causas)",
                    ),
                ),
                (
                    "regular_icu_pediatric",
                    models.PositiveSmallIntegerField(
                        help_text="Informe quantos leitos deste tipo estão ocupados.",
                        verbose_name="Ocupação de leitos UTI pediátrico (outras causas)",
                    ),
                ),
                (
                    "unity",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="app.HealthcareUnity",
                    ),
                ),
            ],
            options={
                "verbose_name": "Entrada de caso",
                "verbose_name_plural": "Entradas de casos",
            },
        ),
        migrations.CreateModel(
            name="Capacity",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    model_utils.fields.AutoCreatedField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name="created",
                    ),
                ),
                (
                    "modified",
                    model_utils.fields.AutoLastModifiedField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name="modified",
                    ),
                ),
                (
                    "beds_adults",
                    models.PositiveSmallIntegerField(
                        help_text="Informe a capacidade total.",
                        verbose_name="Leitos clínicos de adultos",
                    ),
                ),
                (
                    "beds_pediatric",
                    models.PositiveSmallIntegerField(
                        help_text="Informe a capacidade total.",
                        verbose_name="Leitos clínicos pediátricos",
                    ),
                ),
                (
                    "icu_adults",
                    models.PositiveSmallIntegerField(
                        help_text="Informe a capacidade total.",
                        verbose_name="Leitos UTI adulto",
                    ),
                ),
                (
                    "icu_pediatric",
                    models.PositiveSmallIntegerField(
                        help_text="Informe a capacidade total.",
                        verbose_name="Leitos UTI pediátrico",
                    ),
                ),
                (
                    "unity",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="app.HealthcareUnity",
                    ),
                ),
            ],
            options={
                "verbose_name": "Capacidade",
                "verbose_name_plural": "Valores de capacidade",
            },
        ),
    ]
