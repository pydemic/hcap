from django import forms
from django.shortcuts import render
from material.frontend.views import CreateModelView, ListModelView, UpdateModelView

__all__ = [
    "NotifierListModelView",
    "NotifierUpdateModelView",
    "NotifierCreateModelView",
    "notification_history_view",
]


class NotifierCreateOrUpdateMixin:
    def form_valid(self, form: forms.ModelForm, *args, **kwargs):
        save_fn = form.save
        user = self.request.user

        def save():
            obj = save_fn(commit=False)
            obj.notifier = user
            obj.save()
            form.save_m2m()
            return obj

        form.save = save
        return super().form_valid(form, *args, **kwargs)

    def get_form(self, form_class=None):
        form = super().get_form(form_class=None)
        user = self.request.user
        unities = user.healthcare_units.all()

        if len(unities) == 1:
            self.prepare_form_for_single_unit(form, unities[0])
        field: forms.Field = form.fields["unit"]
        field.queryset = unities
        return form

    def prepare_form_for_single_unit(self, form, unit):
        form.initial["unit"] = unit
        field: forms.Field = form.fields["unit"]
        field.disabled = True

        capacity = unit.capacity_notifications.order_by("date").last()
        if capacity:
            for k, v in capacity.capacities.items():
                form.initial.setdefault(k, v)


class NotifierCreateModelView(NotifierCreateOrUpdateMixin, CreateModelView):
    """
    Creates a new notification
    """


class NotifierUpdateModelView(NotifierCreateOrUpdateMixin, UpdateModelView):
    """
    Updates a new notification
    """


class NotifierListModelView(ListModelView):
    """
    List notifications.
    """

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        return qs.filter(notifier=user)


def notification_history_view(request):
    units = request.user.healthcare_units.all()
    return render(request, "app/notification_history.html", {"units": units})
