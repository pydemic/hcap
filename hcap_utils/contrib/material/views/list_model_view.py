from django.urls import reverse
from material.frontend.views.list import ListModelView as MaterialListModelView


class ListModelView(MaterialListModelView):
    label = None
    name = None

    def __init__(self, *args, **kwargs):
        self.label = kwargs.get("label")
        self.name = kwargs.get("name")

        super().__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs = {
            "list_url": f"{self.label}:{self.name}{self.template_name_suffix}",
            "datatable_config": self.get_datatable_config(),
            "headers": self.get_headers_data(),
            "data": self.get_table_data(0, self.paginate_by),
            **kwargs,
        }

        kwargs.setdefault("view", self)

        if self.has_add_permission(self.request):
            kwargs["add_url"] = reverse(f"{self.label}:{self.name}_add")

        if self.extra_context is not None:
            kwargs.update(self.extra_content)

        return kwargs

    def get_item_url(self, item):
        return reverse(f"{self.label}:{self.name}_detail", args=[item.pk])

    def get_template_names(self):
        if self.template_name is None:
            return [
                f"{self.label}/{self.name}{self.template_name_suffix}.html",
                "material/frontend/views/list.html",
            ]

        return [self.template_name]
