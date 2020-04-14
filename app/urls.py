from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.index_view, name="index"),
    path("monitor", views.monitor_view),
    path(
        "historico-de-notificacoes/", views.notification_history_view, name="notification_history"
    ),
    path("aguarde-confirmacao/", views.wait_authorization_message_view, name="wait_confirmation"),
    path(
        "vis/units/<int:cnes_id>/capacity.svg",
        views.plot_healthcare_unit_capacity,
        name="capacity_plot",
    ),
    path("capacidade/", include(views.CapacityViewSet().urls)),
    path("diario/", include(views.LogEntryViewSet().urls)),
    path("notificadores-pendentes/", include(views.NotifierPendingApprovalViewSet().urls)),
    path("unidade-de-saude/", include(views.HealthcareUnitViewSet().urls)),
]
