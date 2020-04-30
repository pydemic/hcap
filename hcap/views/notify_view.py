from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect
from django.views.generic import TemplateView

from hcap import forms


class NotifyView(TemplateView):
    template_name = "hcap/notify.html"

    def get(self, request, *args, **kwargs):
        user = request.user
        return self.render_to_response(
            {
                "active": "capacity",
                "capacity_form": forms.NotifyCapacityForm(user=user),
                "condition_form": forms.NotifyConditionForm(user=user),
            }
        )

    def post(self, request, *args, **kwargs):
        data = request.POST

        action = data.get("action")
        if action == "capacity":
            return self.handle_capacity_action(request, data)
        elif action == "condition":
            return self.handle_condition_action(request, data)
        else:
            return self.get(request, *args, **kwargs)

    def handle_capacity_action(self, request, data):
        user = request.user
        form = forms.NotifyCapacityForm(data, user=user)

        if form.is_valid():
            capacity = form.save()
            return redirect("hcap:healthcare_unit_capacities_list", capacity.healthcare_unit_id)
        else:
            return self.render_to_response(
                {
                    "active": "capacity",
                    "capacity_form": form,
                    "condition_form": forms.NotifyConditionForm(user=user),
                }
            )

    def handle_condition_action(self, request, data):
        user = request.user
        form = forms.NotifyConditionForm(data, user=user)

        if form.is_valid():
            condition = form.save()
            return redirect("hcap:healthcare_unit_conditions_list", condition.healthcare_unit_id)
        else:
            return self.render_to_response(
                {
                    "active": "condition",
                    "capacity_form": forms.NotifyCapacityForm(user=user),
                    "condition_form": form,
                }
            )


notify_view = user_passes_test(lambda u: u.is_authenticated and u.is_notifier)(NotifyView.as_view())
