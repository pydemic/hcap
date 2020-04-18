from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest

from hcap import forms


@login_required
def index_view(request):
    user = request.user

    if user.is_manager:
        return redirect("hcap:notifierforhealthcareunit_list")
    elif user.is_notifier:
        return redirect("hcap:logentry_list")
    elif user.has_pending_authorization:
        return redirect("hcap:wait_confirmation")

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
            return redirect("hcap:wait_confirmation")

    elif request.method == "POST" and request.POST["action"] == "cities":
        active = "cities"
        cities_form = forms.FillCitiesForm(request.POST, user=user)
        if cities_form.is_valid():
            cities_form.save()
            return redirect("hcap:wait_confirmation")

    ctx = {"cnes_form": cnes_form, "cities_form": cities_form, "active": active}
    return render(request, "hcap/index.html", ctx)
