from django.conf.urls import url
from material.frontend.views import ModelViewSet as MaterialModelViewSet

from hcap_utils.contrib.material import views


class ModelViewSet(MaterialModelViewSet):
    label = None
    name = None
    extra_context = None

    def __init__(self, *args, **kwargs):
        if self.label is None:
            self.label = self.model._meta.app_label

        if self.name is None:
            self.name = self.model._meta.model_name

        super().__init__(*args, **kwargs)

    def filter_kwargs(self, view_class, **kwargs):
        extra_context = None
        if self.extra_context is not None:
            extra_context = self.extra_context
        elif hasattr(self, "get_extra_context"):
            extra_context = self.get_extra_context

        kwargs = {
            "label": self.label,
            "name": self.name,
            "extra_context": extra_context,
            **kwargs,
        }
        return super().filter_kwargs(view_class, **kwargs)

    create_view_class = views.CreateModelView

    @property
    def create_view(self):
        return [r"^add/$", self.get_create_view(), "{name}_add"]

    detail_view_class = views.DetailModelView

    @property
    def detail_view(self):
        return [r"^(?P<pk>.+)/detail/$", self.get_detail_view(), "{name}_detail"]

    list_view_class = views.ListModelView

    @property
    def list_view(self):
        return [r"^$", self.get_list_view(), "{name}_list"]

    update_view_class = views.UpdateModelView

    @property
    def update_view(self):
        return [r"^(?P<pk>.+)/change/$", self.get_update_view(), "{name}_change"]

    delete_view_class = views.DeleteModelView

    @property
    def delete_view(self):
        return [r"^(?P<pk>.+)/delete/$", self.get_delete_view(), "{name}_delete"]

    @property
    def urls(self):
        result = []

        format_kwargs = {"name": self.name}

        url_entries = (
            getattr(self, attr)
            for attr in dir(self)
            if attr.endswith("_view")
            if isinstance(getattr(self, attr), (list, tuple))
        )

        for url_entry in url_entries:
            regexp, view, name = url_entry
            result.append(
                url(regexp.format(**format_kwargs), view, name=name.format(**format_kwargs))
            )

        return result
