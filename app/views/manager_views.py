from material.frontend.views import CreateModelView, UpdateModelView

from app import forms


class NotifierPendingApprovalCreateModelView(CreateModelView):
    def has_object_permission(self, request, obj):
        return request.user.state_id == obj.state_id

    form_class = forms.NotifierPendingApprovalForm

    def get_form_kwargs(self):
        return {"manager": self.request.user, **super().get_form_kwargs()}


class NotifierPendingApprovalUpdateModelView(UpdateModelView):
    form_class = forms.NotifierPendingApprovalForm

    def get_form_kwargs(self):
        return {"manager": self.request.user, **super().get_form_kwargs()}

    def get_form(self, form_class=None):
        obj = self.object.notifier
        qs = type(obj).objects.filter(pk=obj.pk)
        form = super().get_form(form_class)
        form.fields["notifier"].disabled = True
        form.fields["notifier"].queryset = qs
        form.initial["notifier"] = obj.pk
        return form
