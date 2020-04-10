from django.urls import path, include
from django.views.generic import RedirectView

import app.views.manager_viewsets
from . import views

urlpatterns = [
    path("", RedirectView.as_view(url="./diario/"), name="index"),
    path("diario/", include(views.LogEntryViewSet().urls)),
    path("capacidade/", include(views.CapacityViewSet().urls)),
    path("unidade-de-saude/", include(app.views.manager_viewsets.HealthcareUnitViewSet().urls)),
]
