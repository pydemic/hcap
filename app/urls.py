from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.index_view, name="index"),
    path("aguarde-confirmacao/", views.wait_authorization_message_view, name="wait_confirmation"),
    path("capacidade/", include(views.CapacityViewSet().urls)),
    path("diario/", include(views.LogEntryViewSet().urls)),
    path("notificadores-pendentes/", include(views.NotifierPendingApprovalViewSet().urls)),
    path("unidade-de-saude/", include(views.HealthcareUnitViewSet().urls)),
    path("vis/units/<int:pk>/capacity.svg", views.plot_healthcare_unit_capacity),
]
