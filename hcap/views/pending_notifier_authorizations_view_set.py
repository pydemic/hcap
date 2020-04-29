from django.db.models import Q
from hcap.forms import PendingNotifierAuthorizationForm
from hcap_accounts.models import HealthcareUnitNotifier, RegionManager
from hcap_geo.models import Region
from hcap_utils.contrib.material.viewsets import ModelViewSet


class PendingNotifierAuthorizationsViewSet(ModelViewSet):
    model = HealthcareUnitNotifier
    label = "hcap"
    name = "pending_notifier_authorizations"

    list_display = ("user", "healthcare_unit", "is_authorized")
    ordering = ("healthcare_unit", "user")

    form_class = PendingNotifierAuthorizationForm

    def get_queryset(self, request):
        user = request.user

        city_ids = list(
            user.region_managers.filter(region__kind=Region.KIND_CITY).values_list(
                "region_id", flat=True
            )
        )

        state_ids = list(
            user.region_managers.filter(region__kind=Region.KIND_STATE).values_list(
                "region_id", flat=True
            )
        )

        country_ids = list(
            user.region_managers.filter(region__kind=Region.KIND_COUNTRY).values_list(
                "region_id", flat=True
            )
        )

        return (
            self.model.objects.exclude(user=user)
            .exclude(is_authorized=True)
            .filter(
                Q(healthcare_unit__city_id__in=city_ids)
                | Q(healthcare_unit__state_id__in=state_ids)
                | Q(healthcare_unit__country_id__in=country_ids)
            )
        )

    def has_add_permission(self, request):
        return False

    def has_view_permission(self, request, obj=None):
        user = request.user
        return user is not None and user.is_authenticated and user.is_manager

    def has_change_permission(self, request, obj=None):
        user = request.user
        return user is not None and user.is_authenticated and user.is_manager

    def has_delete_permission(Self, request, obj=None):
        user = request.user
        return user is not None and user.is_authenticated and user.is_manager
