from hcap_accounts.models import RegionManager
from hcap_utils.contrib.material.viewsets import ModelViewSet


class MyManagerAuthorizationsViewSet(ModelViewSet):
    model = RegionManager
    label = "hcap"
    name = "my_manager_authorizations"

    list_display = ("region", "region_kind", "is_authorized")
    ordering = ("region",)

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

    def has_delete_permission(self, request, obj=None):
        user = request.user
        return user is not None and user.is_authenticated
