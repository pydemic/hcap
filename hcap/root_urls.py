from django.conf import settings
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path("", RedirectView.as_view(url="./hcap/"), name="home"),
    path("dashboard/", RedirectView.as_view(url=settings.GRAFANA_DASHBOARD_URL), name="grafana"),
    path("select2/", include("django_select2.urls")),
    path("accounts/", include("allauth.urls")),
    # Material override routes and must be defined last
    path("", include("material.frontend.urls")),
    path("", include("django_prometheus.urls")),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
