from hcap_accounts.models import HealthcareUnitNotifier, RegionManager
from hcap_notifications.models import HealthcareUnitCondition
from hcap_utils.contrib.material.viewsets import ModelViewSet


class HealthcareUnitConditionsViewSet(ModelViewSet):
    model = HealthcareUnitCondition
    label = "hcap"
    name = "healthcare_unit_conditions"

    list_display = (
        "healthcare_unit",
        "date",
        "total_cases",
        "sari_cases",
        "covid_cases",
        "notifier",
    )

    ordering = ("healthcare_unit", "date")

    def get_queryset(self, request):
        healthcare_unit_id = request.GET.get("healthcare_unit_id")
        return self.model.objects.filter(healthcare_unit_id=healthcare_unit_id)

    def has_add_permission(self, request):
        return False

    def has_view_permission(self, request, obj=None):
        user = request.user
        return user is not None and user.is_authenticated

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        user = request.user
        if user is None:
            return False

        if not user.is_authenticated:
            return False

        valid_notifier = user.is_notifier and obj.notifier.user_id == user.id
        valid_manager = False

        if not valid_notifier:
            region_id = obj.healthcare_unit.region_id
            valid_manager = RegionManager.objects.filter(
                user_id=user.id, region_id=region_id
            ).exists()

        if not valid_notifier and not valid_manager:
            return False

        return True
