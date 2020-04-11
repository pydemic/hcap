from material.frontend.views import CreateModelView, UpdateModelView

from app import forms


class NotifierPendingApprovalCreateModelView(CreateModelView):
    def get_form(self, form_class=None):
        return forms.NotifierPendingApprovalForm(
            manager=self.request.user, **self.get_form_kwargs()
        )


class NotifierPendingApprovalUpdateModelView(UpdateModelView):
    def get_form(self, form_class=None):
        return forms.NotifierPendingApprovalForm(
            manager=self.request.user, **self.get_form_kwargs()
        )
