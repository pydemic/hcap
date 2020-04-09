from django.urls import path, include
from django.views.generic import RedirectView

from . import viewsets


urlpatterns = [
    path("", RedirectView.as_view(url="./diario/"), name="index"),
    path("diario/", include(viewsets.LogEntryViewSet().urls)),
    path("capacidade/", include(viewsets.CapacityViewSet().urls)),
    path("unidade-de-saude/", include(viewsets.HealthcareUnityViewSet().urls)),
]
