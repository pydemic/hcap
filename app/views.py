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
            Row("sari_beds_adults", "covid_cases_adults"),
            Row("sari_beds_pediatric", "covid_cases_pediatric"),
        ),
        Fieldset(
            "Leitos UTI ocupados com pacientes SRAG",
            Row("sari_icu_adults", "covid_casesadults"),
            Row("sari_icu_pediatric", "covid_casespediatric"),
        ),
        Fieldset(
            "Leitos Clínicos (outras causas)",
            Row("regular_beds_adults", "regular_beds_pediatric"),
        ),
        Fieldset(
            "Leitos UTI (outras causas)",
            Row("regular_icu_adults", "regular_icu_pediatric"),
        ),
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
        Fieldset("Leitos clínicos", Row("beds_adults", "beds_pediatric"),),
        Fieldset("Leitos clínicos", Row("icu_adults", "icu_pediatric"),),
    )


class HealthcareUnityViewSet(ModelViewSet):
    model = models.HealthcareUnity

    filters = ("municipality", "is_validated")
    list_display = ("name", "cnes_id", "municipality", "is_validated")
    layout = Layout(
        Fieldset(
            "Características do estabelecimento",
            "name",
            Row("cnes_id", "municipality"),
        ),
        Fieldset(
            "Responsável principal por preenchimento de cadastro",
            "contact",
            Row("email", "phone"),
        ),
    )
