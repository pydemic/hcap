from material import Layout, Fieldset, Row
from material.frontend.views import ModelViewSet

from app import models, views


class HealthcareUnitViewSet(ModelViewSet):
    model = models.HealthcareUnit

    filters = ("city", "is_validated")
    list_display = ("name", "cnes_id", "city", "is_validated")
    layout = Layout(
        Fieldset("Características do estabelecimento", "name", Row("cnes_id", "city")), "notifiers"
    )


class NotifierPendingApprovalViewSet(ModelViewSet):
    model = models.NotifierForHealthcareUnit
    create_view_class = views.NotifierPendingApprovalCreateModelView
    update_view_class = views.NotifierPendingApprovalUpdateModelView
    list_display = ("notifier", "unit", "city", "is_approved")

    def get_queryset(self, request):
        state_id = request.user.state_id
        return (
            self.model.objects.filter(unit__city__state_id=state_id)
            .order_by("is_approved", "notifier__name")
            .select_related("notifier", "unit", "unit__city")
        )

    def has_add_permission(self, request):
        if super().has_change_permission(request):
            return True
        return request.user.is_manager

    def has_view_permission(self, request, obj=None):
        if super().has_view_permission(request, obj):
            return True
        return self._object_permission(request, obj)

    def has_change_permission(self, request, obj=None):
        if super().has_change_permission(request, obj):
            return True
        return self._object_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if super().has_delete_permission(request, obj):
            return True
        return self._object_permission(request, obj)

    def _object_permission(self, request, obj):
        user = request.user
        if not user.is_manager:
            return False
        if obj is not None:
            rel = user.m2m_cities_as_manager.filter(city=obj.unit.city)
            return rel.exists()
        return True

    def city(self, obj):
        return obj.unit.city.name

    city.short_description = "Cidade"
