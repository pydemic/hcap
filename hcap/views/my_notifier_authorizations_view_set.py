from django.contrib.auth.decorators import login_required
from material.frontend.views import ModelViewSet

from hcap_accounts.models import HealthcareUnitNotifier


class MyNotifierAuthorizationsViewSet(ModelViewSet):
    model = HealthcareUnitNotifier
    model._meta.app_label = "hcap"
    model._meta.model_name = "my_notifier_authorizations"

    list_display = ("healthcare_unit", "is_authorized")

    def get_queryset(self, request):
        user = request.user
        return self.model.objects.filter(user=user)

    def has_add_permission(self, request):
        return False

    def has_view_permission(self, request, obj=None):
        return request.user is not None

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(Self, request, obj=None):
        return request.user is not None
