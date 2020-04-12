from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect

from .. import forms

__all__ = ["index_view", "wait_authorization_message_view"]


@login_required
def index_view(request):
    user = request.user
    if user.is_authorized:
        if user.role == user.ROLE_MANAGER:
            return redirect("app:logentry_list")
        elif user.role == user.ROLE_NOTIFIER:
            return redirect("app:logentry_list")

    cnes_form = forms.CNESForm()
    cities_form = forms.FillCitiesForm()
    active = "cnes"

    if request.method == "POST" and request.POST["action"] not in ("cnes", "cities"):
        action = request.POST["action"]
        return HttpResponseBadRequest(f"invalid action: {action}")
    elif request.method == "POST" and request.POST["action"] == "cnes":
        cnes_form = forms.CNESForm(request.POST)
        if cnes_form.is_valid():
            cnes_form.save(user)
    elif request.method == "POST" and request.POST["action"] == "cities":
        active = "cities"
        cities_form = forms.FillCitiesForm(request.POST)
        if cities_form.is_valid():
            cities_form.save(user)

    ctx = {"cnes_form": cnes_form, "cities_form": cities_form, "active": active}
    return render(request, "app/index.html", ctx)


@login_required
def wait_authorization_message_view(request):
    return render(request, "app/wait_authorization.html", {})
