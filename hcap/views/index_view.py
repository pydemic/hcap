from django.contrib.auth.decorators import login_required
from django.shortcuts import reverse
from django.views.generic import RedirectView


class IndexView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        user = self.request.user

        if user.is_manager:
            return reverse("hcap:notifiers")
        elif user.is_notifier:
            return reverse("hcap:my_healthcare_units")
        elif user.has_pending_authorization:
            return reverse("hcap:my_authorizations")
        else:
            return reverse("hcap:request_authorization")


index_view = login_required(IndexView.as_view())
