from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect

from .. import forms

__all__ = ["index_view", "wait_authorization_message_view"]

import logging

log = logging.getLogger("django")


@login_required
def index_view(request):
    user = request.user
    import warnings

    warnings.warn(str(user._wrapped.__dict__))
    if user.is_manager:
        return redirect("app:notifierforhealthcareunit_list")
    elif user.is_notifier:
        return redirect("app:logentry_list")
    elif user.role != user.ROLE_NONE:
        return redirect("app:wait_confirmation")

    cnes_form = forms.CNESForm(request=request)
    cities_form = forms.FillCitiesForm(user=user)
    active = "cnes"

    if request.method == "POST" and request.POST["action"] not in ("cnes", "cities"):
        action = request.POST["action"]
        return HttpResponseBadRequest(f"invalid action: {action}")

    elif request.method == "POST" and request.POST["action"] == "cnes":
        cnes_form = forms.CNESForm(request.POST, request=request)
        if cnes_form.is_valid():
            cnes_form.save(user)
            return redirect("app:wait_confirmation")

    elif request.method == "POST" and request.POST["action"] == "cities":
        active = "cities"
        cities_form = forms.FillCitiesForm(request.POST, user=user)
        if cities_form.is_valid():
            cities_form.save()
            return redirect("app:wait_confirmation")

    ctx = {"cnes_form": cnes_form, "cities_form": cities_form, "active": active}
    return render(request, "app/index.html", ctx)


@login_required
def wait_authorization_message_view(request):
    user = request.user
    if user.role == user.ROLE_NONE:
        return redirect("app:index")
    return render(request, "app/wait_authorization.html", {})
