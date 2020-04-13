from collections import defaultdict
from django.http import HttpResponse, HttpResponseBadRequest
from prometheus_client import CollectorRegistry, Gauge, generate_latest, CONTENT_TYPE_LATEST

from .. import models

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
        units = models.HealthcareUnit.objects.select_related("city", "city__state").all()
        logs = models.LogEntry.objects.select_related(
            "unit", "unit__city", "unit__city__state"
        ).all()

        _build_units_report(units)
        _build_covid_cases_report(logs)

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
        units_report[(unit.is_active, unit.city.state.name)] += 1

    for ref, value in units_report.items():
        labels = {"is_active": ref[0], "uf": ref[1]}
        gauge_healthcare_units.labels(**labels).set(value)


def _build_covid_cases_report(logs):
    last_logs = _filter_last_log_by_cnes(logs)

    for log in last_logs:
        labels = {"city": log.unit.city.name, "uf": log.unit.city.state.name}

        # covid
        gauge_cases_covid_adult.labels(**labels).set(log.cases["covid_cases_adults"])
        gauge_cases_icu_covid_adult.labels(**labels).set(log.cases["icu_covid_cases_adults"])
        gauge_cases_covid_pediatric.labels(**labels).set(log.cases["covid_cases_pediatric"])
        gauge_cases_icu_covid_pediatric.labels(**labels).set(log.cases["icu_covid_cases_pediatric"])

        # sari
        gauge_cases_sari_adult.labels(**labels).set(log.cases["sari_cases_adults"])
        gauge_cases_icu_sari_adult.labels(**labels).set(log.cases["icu_sari_cases_adults"])
        gauge_cases_sari_pediatric.labels(**labels).set(log.cases["sari_cases_pediatric"])
        gauge_cases_icu_sari_pediatric.labels(**labels).set(log.cases["icu_sari_cases_pediatric"])

        # regular
        gauge_cases_regular_adult.labels(**labels).set(log.cases["regular_cases_adults"])
        gauge_cases_icu_regular_adult.labels(**labels).set(log.cases["icu_regular_cases_adults"])
        gauge_cases_regular_pediatric.labels(**labels).set(log.cases["regular_cases_pediatric"])
        gauge_cases_icu_regular_pediatric.labels(**labels).set(
            log.cases["icu_regular_cases_pediatric"]
        )


def _filter_last_log_by_cnes(logs):
    last_logs = {}
    for log in logs:
        if log.unit.cnes_id not in last_logs or last_logs[log.unit.cnes_id].date < log.date:
            last_logs[log.unit.cnes_id] = log

    return last_logs.values()
