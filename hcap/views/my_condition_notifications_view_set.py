from hcap_notifications.models import HealthcareUnitCondition
from hcap_utils.contrib.material.viewsets import ModelViewSet


class MyConditionNotificationsViewSet(ModelViewSet):
    model = HealthcareUnitCondition
    label = "hcap"
    name = "my_condition_notifications"

    list_display = ("healthcare_unit", "date", "total_cases", "sari_cases", "covid_cases")

    ordering = ("healthcare_unit", "-date")

    def get_queryset(self, request):
        return self.model.objects.filter(notifier__user=request.user)

    def has_add_permission(self, request):
        return False

    def has_view_permission(self, request, obj=None):
        user = request.user
        return user is not None and user.is_authenticated and user.is_notifier

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
