from material import Layout, Row, Fieldset
from material.frontend.views import ModelViewSet

from . import models
from . import views


class HealthcareUnityStateMixin(ModelViewSet):
    create_view_class = views.CreateLogEntryView
    list_display = ("unity", "date", "icu_total_", "clinic_total_")

    def icu_total_(self, obj):
        return obj.icu_total

    icu_total_.short_description = "Total UTI"

    def clinic_total_(self, obj):
        try:
            return obj.beds_total
        except AttributeError:
            return obj.cases_total

    clinic_total_.short_description = "Total Clínicos"


class LogEntryViewSet(HealthcareUnityStateMixin, ModelViewSet):
    model = models.LogEntry
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
        Fieldset("Leitos UTI (outras causas)", Row("icu_regular_adults", "icu_regular_pediatric")),
    )


class CapacityViewSet(HealthcareUnityStateMixin, ModelViewSet):
    model = models.Capacity
    create_view_class = views.CreateCapacityView
    layout = Layout(
        "unity",
        "date",
        Fieldset("Leitos clínicos/enfermaria", Row("beds_adults", "beds_pediatric")),
        Fieldset("Leitos UTI", Row("icu_adults", "icu_pediatric")),
    )


class HealthcareUnityViewSet(ModelViewSet):
    model = models.HealthcareUnity

    filters = ("municipality", "is_validated")
    list_display = ("name", "cnes_id", "municipality", "is_validated")
    layout = Layout(
        Fieldset("Características do estabelecimento", "name", Row("cnes_id", "municipality")),
        "notifiers",
    )
