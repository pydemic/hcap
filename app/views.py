from material import Layout, Row, Fieldset
from material.frontend.views import ModelViewSet

from . import models


class LogEntryViewSet(ModelViewSet):
    model = models.LogEntry

    list_display = ("unity", "date")
    layout = Layout(
        "unity",
        "date",
        Fieldset(
            "Leitos Clínicos ocupados com pacientes SRAG",
            Row("sari_cases_adults", "covid_cases_adults"),
            Row("sari_cases_pediatric", "covid_cases_pediatric"),
        ),
        Fieldset(
            "Leitos UTI ocupados com pacientes SRAG",
            Row("icu_sari_cases_adults", "icu_covid_cases_adults"),
            Row("icu_sari_cases_pediatric", "icu_covid_cases_pediatric"),
        ),
        Fieldset(
            "Leitos Clínicos (outras causas)",
            Row("regular_cases_adults", "regular_cases_pediatric"),
        ),
        Fieldset("Leitos UTI (outras causas)", Row("regular_icu_adults", "regular_icu_pediatric"),),
    )


class CapacityViewSet(ModelViewSet):
    model = models.Capacity
    list_display = (
        "unity",
        "beds_adults",
        "beds_pediatric",
        "icu_adults",
        "icu_pediatric",
    )
    layout = Layout(
        "unity",
        "date",
        Fieldset("Leitos clínicos/enfermaria", Row("beds_adults", "beds_pediatric"),),
        Fieldset("Leitos UTI", Row("icu_adults", "icu_pediatric"),),
    )


class HealthcareUnityViewSet(ModelViewSet):
    model = models.HealthcareUnity

    filters = ("municipality", "is_validated")
    list_display = ("name", "cnes_id", "municipality", "is_validated")
    layout = Layout(
        Fieldset("Características do estabelecimento", "name", Row("cnes_id", "municipality"),),
        "notifiers",
    )
