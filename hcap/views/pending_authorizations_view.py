from django.contrib.auth.decorators import user_passes_test
from django.views.generic import TemplateView


class PendingAuthorizationsView(TemplateView):
    template_name = "hcap/pending_authorizations.html"


pending_authorizations_view = user_passes_test(lambda u: u.is_authenticated and u.is_manager)(
    PendingAuthorizationsView.as_view()
)
