from django.urls import reverse
from django.utils.html import format_html
from django.utils.text import capfirst
from django.db.models import AutoField
from material.frontend.views.detail import DetailModelView as MaterialDetailModelView


class DetailModelView(MaterialDetailModelView):
    label = None
    name = None

    def __init__(self, *args, **kwargs):
        self.label = kwargs.get("label")
        self.name = kwargs.get("name")
        self.extra_context = kwargs.get("extra_context")

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
            kwargs["change_url"] = f"{self.label}:{self.name}_change"

        if self.has_delete_permission(self.request, self.object):
            kwargs["delete_url"] = f"{self.label}:{self.name}_delete"

        if self.extra_context is not None:
            if callable(self.extra_context):
                kwargs.update(self.extra_context(self.request))
            else:
                kwargs.update(self.extra_context)

        return kwargs

    def get_object_data(self):
        for field in self.object._meta.fields:
            if isinstance(field, AutoField):
                continue
            elif field.auto_created:
                continue
            else:
                choice_display_attr = "get_{}_display".format(field.name)
            if hasattr(self.object, choice_display_attr):
                value = getattr(self.object, choice_display_attr)()
            else:
                value = getattr(self.object, field.name)

            if value is not None:
                if isinstance(value, bool):
                    value = format_html(
                        '<i class="material-icons">{}</i>'.format("check" if value else "close")
                    )
                yield (capfirst(field.verbose_name), value)

    def get_template_names(self):
        if self.template_name is None:
            return [
                f"{self.label}/{self.name}{self.template_name_suffix}.html",
                "material/frontend/views/detail.html",
            ]

        return [self.template_name]
