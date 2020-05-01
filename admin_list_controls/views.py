import os
import json
from django.conf import settings
from django.utils.safestring import mark_safe
from wagtail.contrib.modeladmin.views import IndexView
from .controls import ListControls, Layout
from .vendor import webpack_manifest


class ListControlsIndexViewMixin:
    """
    Adds filtering, sorting and other controls to a modeladmin's list/index view
    """

    _built_list_controls = None
    _items_per_page = None

    def build_list_controls(self):
        """
        A hook provided to declare the filters for the UI
        """
        return ListControls([])

    def apply_list_controls_to_queryset(self, queryset):
        """
        A hook provided to modify the queryset
        """
        return queryset

    def get_list_controls(self):
        if not self._built_list_controls:
            self._built_list_controls = self.build_list_controls()
        return self._built_list_controls

    def get_selected_list_control_layout(self):
        for obj in self.get_list_controls().flatten_hierarchy():
            if obj.object_type == Layout.object_type and obj.is_selected:
                return obj

    def get_template_names(self):
        return ['admin_list_controls/admin_list_controls.html'] + super().get_template_names()

    def get_filters_params(self, params=None):
        """
        Prevent the modeladmin's built-in querying from raising errors when it encounters
        our custom GET data
        """
        params = super().get_filters_params(params)

        for obj in self.get_list_controls().flatten_hierarchy():
            name = getattr(obj, 'name', None)
            if name and name in params:
                del params[name]
        return params

    def get_search_results(self, *args, **kwargs):
        queryset = super().get_search_results(*args, **kwargs)
        queryset = self.apply_list_controls_to_queryset(queryset)
        return queryset

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        # Consumed by the front-end code to build the UI
        context_data['admin_list_controls'] = {
            'initial_state': json.dumps({
                'admin_list_controls': self.get_list_controls().serialize(),
            }),
            'selected_layout': self.get_selected_list_control_layout(),
            'widget_js': self.get_list_controls_widget_js(),
        }

        return context_data

    def get_list_controls_widget_js(self):
        manifest_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 'webpack_manifest.json',
        )
        manifest = webpack_manifest.load(
            path=manifest_path,
            static_url=settings.STATIC_URL,
            static_root=settings.STATIC_ROOT,
            debug=settings.DEBUG,
        )
        return mark_safe(str(manifest.admin_list_controls.js))


class ListControlsIndexView(ListControlsIndexViewMixin, IndexView):
    pass
