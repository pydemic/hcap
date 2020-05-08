from django.utils.translation import gettext_lazy as _

from hcap_notifications.models import HealthcareUnitCondition
from hcap_utils.contrib.material.viewsets import ModelViewSet
from hcap_utils.properties import trans_property


class MyConditionNotificationsViewSet(ModelViewSet):
    model = HealthcareUnitCondition
    label = "hcap"
    name = "my_condition_notifications"

    list_display = ("healthcare_unit", "date", "_total_cases", "_sari_cases", "_covid_cases")

    ordering = ("healthcare_unit", "-date")

    @trans_property(_("Total Cases"))
    def _total_cases(self):
        self.total_cases

    @trans_property(_("Sari Cases"))
    def _sari_cases(self):
        self.sari_cases

    @trans_property(_("Covid Cases"))
    def _covid_cases(self):
        self.codiv_cases

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
