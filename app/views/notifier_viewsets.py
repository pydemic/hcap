from material import Layout, Fieldset, Row
from material.frontend.views import ModelViewSet

from .notifier_views import NotifierCreateModelView, NotifierListModelView
from .. import models

__all__ = ["LogEntryViewSet", "CapacityViewSet"]


class NotifierBaseViewSet(ModelViewSet):
    create_view_class = NotifierCreateModelView
    list_view_class = NotifierListModelView
    list_display = ("unit", "date", "icu_total_", "clinic_total_")

    def icu_total_(self, obj):
        return obj.icu_total

    icu_total_.short_description = "Total UTI"

    def clinic_total_(self, obj):
        try:
            return obj.beds_total
        except AttributeError:
            return obj.cases_total

    clinic_total_.short_description = "Total Clínicos"

    #
    # Permissions
    #
    def has_view_permission(self, request, obj=None):
        if super().has_view_permission(request, obj=obj):
            return True

        user = request.user
        if obj is None:
            return user.is_notifier
        elif user.is_notifier:
            return obj.notifier == user

    def has_add_permission(self, request):
        if super().has_add_permission(request):
            return True
        return request.user.is_notifier

    # def has_object_permission(self, request, obj):
    #     return True
    #     if not self.has_add_permission(request):
    #         return False
    #     elif obj.notifier != request.user:
    #         return False
    #     return (obj.created - now()).hours < 20


class LogEntryViewSet(NotifierBaseViewSet):
    model = models.LogEntry
    layout = Layout(
        "unit",
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


class CapacityViewSet(NotifierBaseViewSet):
    model = models.Capacity
    layout = Layout(
        "unit",
        "date",
        Fieldset("Leitos clínicos/enfermaria", Row("beds_adults", "beds_pediatric")),
        Fieldset("Leitos UTI", Row("icu_adults", "icu_pediatric")),
    )
