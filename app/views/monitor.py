from collections import defaultdict
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from prometheus_client import CollectorRegistry, Gauge, generate_latest, CONTENT_TYPE_LATEST

from .. import models

registry = CollectorRegistry()

gauge_healthcare_units = Gauge(
    "healthcare_units",
    "Healthcare unit state by UF (inactive or active)",
    ["uf", "is_active"],
    registry=registry,
)


def monitor_view(request):
    if request.method == "GET":
        units = models.HealthcareUnit.objects.select_related("city", "city__state").all()
        _build_units_report(units)

        metrics_page = generate_latest(registry)
        return HttpResponse(metrics_page, content_type=CONTENT_TYPE_LATEST)

    return HttpResponseBadRequest(f"Invalid method {request.method}")


def _build_units_report(units):
    units_report = defaultdict(int)
    for unit in units:
        units_report[(unit.is_active, unit.city.state.name)] += 1

    for ref, value in units_report.items():
        labels = {"is_active": ref[0], "uf": ref[1]}

        gauge_healthcare_units.labels(**labels).set(value)
