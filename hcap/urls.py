from django.conf import settings
from django.urls import include, path, re_path
from django.utils.translation import gettext as __

from hcap import views


urlpatterns = [
    path("", views.index_view, name="index"),
    path(
        __("request-authorization/"), views.request_authorization_view, name="request_authorization"
    ),
    path(__("my-authorizations/"), views.my_authorizations_view, name="my_authorizations"),
    path(__("my-authorizations/manager/"), include(views.MyManagerAuthorizationsViewSet().urls)),
    path(__("my-authorizations/notifier/"), include(views.MyNotifierAuthorizationsViewSet().urls)),
    path(
        __("pending-authorizations/"),
        views.pending_authorizations_view,
        name="pending_authorizations",
    ),
    path(
        __("pending-authorizations/manager/"),
        include(views.PendingManagerAuthorizationsViewSet().urls),
    ),
    path(
        __("pending-authorizations/notifier/"),
        include(views.PendingNotifierAuthorizationsViewSet().urls),
    ),
    path(__("notify/"), views.notify_view, name="notify"),
    path(
        __(r"healthcare-units/<str:healthcare_unit_id>/capacities/"),
        include(views.HealthcareUnitCapacitiesViewSet().urls),
    ),
    path(
        __(r"healthcare-units/<str:healthcare_unit_id>/conditions/"),
        include(views.HealthcareUnitConditionsViewSet().urls),
    ),
    path(__("healthcare-units/"), include(views.HealthcareUnitsViewSet().urls)),
]
