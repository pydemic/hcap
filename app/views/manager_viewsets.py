from django.contrib.auth import get_user_model
from material import Layout, Fieldset, Row
from material.frontend.views import ModelViewSet

from app import models, views


class HealthcareUnitViewSet(ModelViewSet):
    model = models.HealthcareUnit

    filters = ("city", "is_validated")
    list_display = ("name", "cnes_id", "city", "is_validated")
    layout = Layout(
        Fieldset("Características do estabelecimento", "name", Row("cnes_id", "city")), "notifiers",
    )


class NotifierPendingApprovalViewSet(ModelViewSet):
    model = models.NotifierForHealthcareUnit
    create_view_class = views.NotifierPendingApprovalCreateModelView
    update_view_class = views.NotifierPendingApprovalUpdateModelView
    list_display = ("notifier", "unit")

    def get_queryset(self, request):
        state_id = request.user.state_id
        return self.model.objects.filter(unit__city__state_id=state_id, is_approved=False)

    def has_add_permission(self, request):
        user = request.user
        return user.is_manager or user.is_staff or user.is_superuser

    def has_view_permission(self, request, obj=None):
        return self.has_add_permission(request)

    def has_change_permission(self, request, obj=None):
        return self.has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        return self.has_add_permission(request)
