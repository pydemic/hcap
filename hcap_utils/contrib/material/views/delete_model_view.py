from django.urls import reverse
from material.frontend.views.delete import DeleteModelView as MaterialDeleteModelView


class DeleteModelView(MaterialDeleteModelView):
    label = None
    name = None

    def __init__(self, *args, **kwargs):
        self.label = kwargs.get("label")
        self.name = kwargs.get("name")

        super().__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs = {
            "list_url": f"{self.label}:{self.name}_list",
            "detail_url": f"{self.label}:{self.name}_detail",
        }

        return super().get_context_data(**kwargs)

    def get_success_url(self):
        if self.success_url is None:
            return reverse(f"{self.label}:{self.name}_list")

        return self.success_url

    def get_template_names(self):
        if self.template_name is None:
            return [
                f"{self.label}/{self.name}{self.template_name_suffix}.html",
                "material/frontend/views/confirm_delete.html",
            ]

        return [self.template_name]
