from django.contrib.auth.decorators import user_passes_test
from django.views.generic import TemplateView


class MyNotificationsView(TemplateView):
    template_name = "hcap/my_notifications.html"


my_notifications_view = user_passes_test(lambda u: u.is_authenticated and u.is_notifier)(
    MyNotificationsView.as_view()
)
