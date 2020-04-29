from hcap.forms import PendingManagerAuthorizationForm
from hcap_accounts.models import RegionManager
from hcap_utils.contrib.material.viewsets import ModelViewSet


class PendingManagerAuthorizationsViewSet(ModelViewSet):
    model = RegionManager
    label = "hcap"
    name = "pending_manager_authorizations"

    list_display = ("user", "is_authorized", "region", "region_kind")
    ordering = ("region", "user")

    form_class = PendingManagerAuthorizationForm

    def get_queryset(self, request):
        user = request.user
        region_ids = list(self.model.objects.filter(user=user).values_list("region_id", flat=True))
        result = self.model.objects.filter(region_id__in=region_ids, is_authorized=False).exclude(
            user=user
        )
        return result

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
