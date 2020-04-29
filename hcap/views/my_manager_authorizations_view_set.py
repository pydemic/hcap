from material.frontend.views import ModelViewSet

from hcap_accounts.models import RegionManager


class MyManagerAuthorizationsViewSet(ModelViewSet):
    model = RegionManager
    model._meta.app_label = "hcap"
    model._meta.model_name = "my_manager_authorizations"

    list_display = ("region", "region_kind", "is_authorized")
    ordering = ("region",)

    def get_queryset(self, request):
        user = request.user
        return self.model.objects.filter(user=user)

    def has_add_permission(self, request):
        return False

    def has_view_permission(self, request, obj=None):
        return request.user is not None

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(Self, request, obj=None):
        return request.user is not None
