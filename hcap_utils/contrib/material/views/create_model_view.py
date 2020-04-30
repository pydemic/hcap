from django.contrib import messages
from django.urls import reverse
from django.utils.encoding import force_text
from django.utils.html import format_html
from django.utils.http import urlquote
from django.utils.translation import ugettext_lazy as _
from material.frontend.views.create import CreateModelView as MaterialCreateModelView


class CreateModelView(MaterialCreateModelView):
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
            "detail_url": f"{self.label}:{self.name}_detail",
        }

        kwargs.setdefault("view", self)

        if "form" not in kwargs:
            kwargs["form"] = self.get_form()

        if self.extra_context is not None:
            if callable(self.extra_context):
                kwargs.update(self.extra_context(self.request))
            else:
                kwargs.update(self.extra_context)

        return kwargs

    def get_success_url(self):
        if self.success_url is None:
            return reverse(f"{self.label}:{self.name}_detail", args=[self.object.pk])

        return self.success_url

    def get_template_names(self):
        if self.template_name is None:
            return [
                f"{self.label}/{self.name}{self.template_name_suffix}.html",
                f"{self.label}/{self.name}_form.html",
                "material/frontend/views/form.html",
            ]

        return [self.template_name]

    def report(self, message, level=messages.INFO, fail_silently=True, **kwargs):
        url = reverse(f"{self.label}:{self.name}_detail", args=[self.object.pk])
        link = format_html('<a href="{}">{}</a>', urlquote(url), force_text(self.object))

        name = force_text(self.model._meta.verbose_name)

        options = {"link": link, "name": name}
        options.update(kwargs)

        message = format_html(_(message).format(**options))
        messages.add_message(self.request, level, message, fail_silently=True)
