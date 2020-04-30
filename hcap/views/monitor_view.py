from collections import defaultdict
from django.http import HttpResponse, HttpResponseBadRequest
from prometheus_client import CollectorRegistry, Gauge, generate_latest, CONTENT_TYPE_LATEST

from hcap_institutions.models import HealthcareUnit
from hcap_notifications.models import HealthcareUnitCondition

registry = CollectorRegistry()

# metrics definition
gauge_healthcare_units = Gauge(
    "healthcare_units",
    "Healthcare unit state by UF (inactive or active)",
    ["uf", "is_active"],
    registry=registry,
)

gauge_cases_covid_adult = Gauge(
    "cases_covid_adult_daily", "Covid daily adult cases", ["uf", "city"], registry=registry
)

gauge_cases_icu_covid_adult = Gauge(
    "cases_icu_covid_adult_daily", "ICU covid daily adult cases", ["uf", "city"], registry=registry
)

gauge_cases_covid_pediatric = Gauge(
    "cases_covid_pediatric_daily", "Covid daily pediatric cases", ["uf", "city"], registry=registry
)

gauge_cases_icu_covid_pediatric = Gauge(
    "cases_icu_covid_pediatric_daily",
    "ICU covid daily pediatric cases",
    ["uf", "city"],
    registry=registry,
)

gauge_cases_sari_adult = Gauge(
    "cases_sari_adult_daily", "Covid daily adult cases", ["uf", "city"], registry=registry
)

gauge_cases_icu_sari_adult = Gauge(
    "cases_icu_sari_adult_daily", "ICU sari daily adult cases", ["uf", "city"], registry=registry
)

gauge_cases_sari_pediatric = Gauge(
    "cases_sari_pediatric_daily", "Covid daily pediatric cases", ["uf", "city"], registry=registry
)

gauge_cases_icu_sari_pediatric = Gauge(
    "cases_icu_sari_pediatric_daily",
    "ICU sari daily pediatric cases",
    ["uf", "city"],
    registry=registry,
)


gauge_cases_regular_adult = Gauge(
    "cases_regular_adult_daily", "Covid daily adult cases", ["uf", "city"], registry=registry
)

gauge_cases_icu_regular_adult = Gauge(
    "cases_icu_regular_adult_daily",
    "ICU regular daily adult cases",
    ["uf", "city"],
    registry=registry,
)

gauge_cases_regular_pediatric = Gauge(
    "cases_regular_pediatric_daily",
    "Covid daily pediatric cases",
    ["uf", "city"],
    registry=registry,
)

gauge_cases_icu_regular_pediatric = Gauge(
    "cases_icu_regular_pediatric_daily",
    "ICU regular daily pediatric cases",
    ["uf", "city"],
    registry=registry,
)


def monitor_view(request):
    if request.method == "GET":
        units = HealthcareUnit.objects.select_related("city", "state").all()
        conditions = HealthcareUnitCondition.objects.select_related(
            "healthcare_unit", "healthcare_unit__city", "healthcare_unit__state"
        ).all()

        _build_units_report(units)
        _build_covid_cases_report(conditions)

        metrics_page = generate_latest(registry)
        if request.GET.get("html") == "true":
            raw = metrics_page.decode("utf-8")
            data = f"<body><pre>{raw}</pre></body>"
            return HttpResponse(data)
        return HttpResponse(metrics_page, content_type=CONTENT_TYPE_LATEST)

    return HttpResponseBadRequest(f"Invalid method {request.method}")


def _build_units_report(units):
    units_report = defaultdict(int)
    for unit in units:
        units_report[(unit.is_active, unit.state.name)] += 1

    for ref, value in units_report.items():
        labels = {"is_active": ref[0], "uf": ref[1]}
        gauge_healthcare_units.labels(**labels).set(value)


def _build_covid_cases_report(conditions):
    last_conditions = _filter_last_condition_by_cnes(conditions)

    for condition in last_conditions:
        labels = {
            "city": condition.healthcare_unit.city.name,
            "uf": condition.healthcare_unit.state.name,
        }

        # covid
        gauge_cases_covid_adult.labels(**labels).set(condition.covid_adult_clinical_cases)
        gauge_cases_icu_covid_adult.labels(**labels).set(condition.covid_adult_icu_cases)
        gauge_cases_covid_pediatric.labels(**labels).set(condition.covid_pediatric_clinical_cases)
        gauge_cases_icu_covid_pediatric.labels(**labels).set(condition.covid_pediatric_icu_cases)

        # sari
        gauge_cases_sari_adult.labels(**labels).set(condition.sari_adult_clinical_cases)
        gauge_cases_icu_sari_adult.labels(**labels).set(condition.sari_adult_icu_cases)
        gauge_cases_sari_pediatric.labels(**labels).set(condition.sari_pediatric_clinical_cases)
        gauge_cases_icu_sari_pediatric.labels(**labels).set(condition.sari_pediatric_icu_cases)

        # regular
        gauge_cases_regular_adult.labels(**labels).set(condition.general_adult_clinical_cases)
        gauge_cases_icu_regular_adult.labels(**labels).set(condition.general_adult_icu_cases)
        gauge_cases_regular_pediatric.labels(**labels).set(
            condition.general_pediatric_clinical_cases
        )
        gauge_cases_icu_regular_pediatric.labels(**labels).set(
            condition.general_pediatric_icu_cases
        )


def _filter_last_condition_by_cnes(conditions):
    last_conditions = {}
    for condition in conditions:
        if (
            condition.healthcare_unit.cnes_id not in last_conditions
            or last_conditions[condition.healthcare_unit.cnes_id].date < condition.date
        ):
            last_conditions[condition.healthcare_unit.cnes_id] = condition

    return last_conditions.values()
