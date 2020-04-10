from material import Layout, Fieldset, Row
from material.frontend.views import ModelViewSet

from app import models


class HealthcareUnitViewSet(ModelViewSet):
    model = models.HealthcareUnit

    filters = ("municipality", "is_validated")
    list_display = ("name", "cnes_id", "municipality", "is_validated")
    layout = Layout(
        Fieldset("Características do estabelecimento", "name", Row("cnes_id", "municipality")),
        "notifiers",
    )
