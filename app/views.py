from django import forms
from django.conf import settings
from django.utils.timezone import now
from material.frontend.views import CreateModelView


class NotifierMixin(CreateModelView):
    def has_add_permission(self, request):
        user = request.user
        if not (user.is_verified_notifier or settings.DEBUG and user.is_superuser):
            return False
        return user.healthcare_unities.exists()

    def has_object_permission(self, request, obj):
        if not self.has_add_permission(request):
            return False
        elif obj.notifier != request.user:
            return False
        return (obj.created - now()).hours < 20

    def form_valid(self, form: forms.ModelForm, *args, **kwargs):
        save_fn = form.save

        def save():
            obj = save_fn(commit=False)
            obj.notifier = self.request.user
            obj.save()
            form.save_m2m()
            return obj

        form.save = save
        return super().form_valid(form, *args, **kwargs)


class CreateCapacityView(NotifierMixin, CreateModelView):
    def get_form(self, form_class=None):
        form = super().get_form(form_class=None)
        user = self.request.user
        unities = list(user.healthcare_unities.all())

        if len(unities) == 1:
            self.prepare_form_for_unity(form, unities[0])
        return form

    def prepare_form_for_unity(self, form, unity):
        form.initial['unity'] = unity
        field: forms.Field = form.fields['unity']
        field.disabled = True

        capacity = unity.capacity_notifications.order_by('date').last()
        if capacity:
            for k, v in capacity.capacities.items():
                form.initial.setdefault(k, v)
