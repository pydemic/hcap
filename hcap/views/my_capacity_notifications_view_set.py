from django.utils.translation import gettext_lazy as _

from hcap_notifications.models import HealthcareUnitCapacity
from hcap_utils.contrib.material.viewsets import ModelViewSet
from hcap_utils.properties import trans_property


class MyCapacityNotificationsViewSet(ModelViewSet):
    model = HealthcareUnitCapacity
    label = "hcap"
    name = "my_capacity_notifications"

    list_display = ("healthcare_unit", "date", "_total_clinical_beds", "_total_icu_beds")

    ordering = ("healthcare_unit", "-date")

    @trans_property(_("Total clinical beds"))
    def _total_clinical_beds(self):
        self.total_clinical_beds

    @trans_property(_("Total icu beds"))
    def _total_icu_beds(self):
        self.total_icu_beds

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
