from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from hcap import forms


class RequestAuthorizationView(TemplateView):
    template_name = "hcap/request_authorization.html"

    def get(self, request, *args, **kwargs):
        user = request.user
        return self.render_to_response(
            {
                "active": "notifier",
                "manager_state_form": forms.ManagerStateAuthorizationRequestForm(user=user),
                "notifier_form": forms.NotifierAuthorizationRequestForm(user=user),
            }
        )

    def post(self, request, *args, **kwargs):
        data = request.POST

        action = data.get("action")
        if action == "notifier":
            return self.handle_notifier_action(request, data)
        elif action == "manager_state":
            return self.handle_manager_state_action(request, data)
        elif action == "manager_cities":
            return self.handle_manager_cities_action(request, data)
        else:
            return self.get(request, *args, **kwargs)

    def handle_notifier_action(self, request, data):
        user = request.user
        form = forms.NotifierAuthorizationRequestForm(data, user=user)

        if form.is_valid():
            form.save()
            return redirect("hcap:my_notifier_authorizations_list")
        else:
            return self.render_to_response(
                {
                    "active": "notifier",
                    "manager_state_form": forms.ManagerStateAuthorizationRequestForm(user=user),
                    "notifier_form": form,
                }
            )

    def handle_manager_state_action(self, request, data):
        user = request.user
        form = forms.ManagerStateAuthorizationRequestForm(data, user=user)

        if form.is_valid():
            if form.is_cities_request():
                return self.render_to_response(
                    {
                        "active": "manager",
                        "manager_cities_form": forms.ManagerCitiesAuthorizationRequestForm(
                            user=user, state_id=form.get_state().id
                        ),
                        "notifier_form": forms.NotifierAuthorizationRequestForm(user=user),
                    }
                )
            else:
                form.save()
                return redirect("hcap:my_manager_authorizations_list")
        else:
            return self.render_to_response(
                {
                    "active": "manager",
                    "manager_state_form": form,
                    "notifier_form": forms.NotifierAuthorizationRequestForm(user=user),
                }
            )

    def handle_manager_cities_action(self, request, data):
        user = request.user
        state_id = data.get("state_hidden")
        form = forms.ManagerCitiesAuthorizationRequestForm(data, user=user, state_id=state_id)

        if form.is_valid():
            form.save()
            return redirect("hcap:my_manager_authorizations_list")
        else:
            return self.render_to_response(
                {
                    "active": "manager",
                    "manager_cities_form": form,
                    "notifier_form": forms.NotifierAuthorizationRequestForm(user=user),
                }
            )


request_authorization_view = login_required(RequestAuthorizationView.as_view())
