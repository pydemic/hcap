from django.urls import reverse
from material.frontend.views.detail import DetailModelView as MaterialDetailModelView


class DetailModelView(MaterialDetailModelView):
    label = None
    name = None

    def __init__(self, *args, **kwargs):
        self.label = kwargs.get("label")
        self.name = kwargs.get("name")

        super().__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs = {
            "list_url": f"{self.label}:{self.name}_list",
            "object_data": self.get_object_data(),
            **kwargs,
        }

        kwargs.setdefault("view", self)

        if self.object:
            kwargs["object"] = self.object
            context_object_name = self.get_context_object_name(self.object)
            if context_object_name:
                kwargs[context_object_name] = self.object

        if self.has_change_permission(self.request, self.object):
            kwargs["change_url"] = reverse(
                f"{self.label}:{self.name}_change", args=[self.object.pk]
            )

        if self.has_delete_permission(self.request, self.object):
            kwargs["delete_url"] = reverse(
                f"{self.label}:{self.name}_delete", args=[self.object.pk]
            )

        return kwargs

    def get_template_names(self):
        if self.template_name is None:
            return [
                f"{self.label}/{self.name}{self.template_name_suffix}.html",
                "material/frontend/views/detail.html",
            ]

        return [self.template_name]
