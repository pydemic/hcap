from django.utils.translation import gettext_lazy as _

from hcap.forms import HealthcareUnitCapacityForm
from hcap_accounts.models import HealthcareUnitNotifier, RegionManager
from hcap_notifications.models import HealthcareUnitCapacity
from hcap_utils.contrib.material.viewsets import ModelViewSet


class HealthcareUnitCapacitiesViewSet(ModelViewSet):
    model = HealthcareUnitCapacity
    label = "hcap"
    name = "healthcare_unit_capacities"

    list_display = (
        "healthcare_unit",
        "date",
        "total_clinical_beds",
        "total_icu_beds",
    )

    ordering = ("healthcare_unit", "-date")

    form_class = HealthcareUnitCapacityForm

    def get_extra_context(self, request):
        healthcare_unit_id = request.path.split("/")[3]
        return {"healthcare_unit_id": healthcare_unit_id, "item_args": [healthcare_unit_id]}

    def get_queryset(self, request):
        return self.model.objects.filter(healthcare_unit_id=request.path.split("/")[3])

    def has_add_permission(self, request):
        return False

    def has_view_permission(self, request, obj=None):
        user = request.user
        return user is not None and user.is_authenticated

    def has_change_permission(self, request, obj=None):
        return self.has_delete_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if (obj.updated_at - obj.created_at).days > 0:
            return False

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
