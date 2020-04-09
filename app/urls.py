from django.urls import path, include
from django.views.generic import RedirectView

from . import views


urlpatterns = [
    path("", RedirectView.as_view(url="./diario/"), name="index"),
    path("diario/", include(views.LogEntryViewSet().urls)),
    path("capacidade/", include(views.CapacityViewSet().urls)),
    path("unidade-de-saude/", include(views.HealthcareUnityViewSet().urls)),
]
