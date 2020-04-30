from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView


class MyAuthorizationsView(TemplateView):
    template_name = "hcap/my_authorizations.html"


my_authorizations_view = login_required(MyAuthorizationsView.as_view())
