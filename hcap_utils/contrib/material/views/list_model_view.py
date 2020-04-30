from django.urls import reverse
from material.frontend.views.list import ListModelView as MaterialListModelView


class ListModelView(MaterialListModelView):
    label = None
    name = None

    def __init__(self, *args, **kwargs):
        self.label = kwargs.get("label")
        self.name = kwargs.get("name")
        self.extra_context = kwargs.get("extra_context")

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
            kwargs["add_url"] = f"{self.label}:{self.name}_add"

        if self.extra_context is not None:
            if callable(self.extra_context):
                kwargs.update(self.extra_context(self.request))
            else:
                kwargs.update(self.extra_context)

        return kwargs

    def get_item_url(self, item):
        args = []

        extra_context = None

        if callable(self.extra_context):
            extra_context = self.extra_context(self.request)
        else:
            extra_context = self.extra_context

        if extra_context is not None:
            item_args = extra_context.get("item_args", [])
            args += item_args

        args += [item.pk]

        return reverse(f"{self.label}:{self.name}_detail", args=args)

    def get_template_names(self):
        if self.template_name is None:
            return [
                f"{self.label}/{self.name}{self.template_name_suffix}.html",
                "material/frontend/views/list.html",
            ]

        return [self.template_name]
