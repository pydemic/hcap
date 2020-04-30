from hcap_accounts.models import HealthcareUnitNotifier
from hcap_utils.contrib.material.viewsets import ModelViewSet


class MyNotifierAuthorizationsViewSet(ModelViewSet):
    model = HealthcareUnitNotifier
    label = "hcap"
    name = "my_notifier_authorizations"

    list_display = ("healthcare_unit", "is_authorized")

    def get_queryset(self, request):
        user = request.user
        return self.model.objects.filter(user=user)

    def has_add_permission(self, request):
        return False

    def has_view_permission(self, request, obj=None):
        user = request.user
        return user is not None and user.is_authenticated

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(Self, request, obj=None):
        user = request.user
        return user is not None and user.is_authenticated
