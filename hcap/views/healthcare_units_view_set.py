from hcap_institutions.models import HealthcareUnit
from hcap_utils.contrib.material.viewsets import ModelViewSet


class HealthcareUnitsViewSet(ModelViewSet):
    model = HealthcareUnit
    label = "hcap"
    name = "healthcare_units"

    list_display = ("cnes_id", "name", "city", "state")
    ordering = ("state", "city", "name")

    def has_add_permission(self, request):
        return False

    def has_view_permission(self, request, obj=None):
        user = request.user
        return user is not None and user.is_authenticated

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
