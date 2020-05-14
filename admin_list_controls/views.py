import os
import json
from collections import Iterable

from django.conf import settings
from django.utils.safestring import mark_safe
from wagtail.contrib.modeladmin.views import IndexView
from .components import ListControls
from .selectors import LayoutSelector
from .vendor import webpack_manifest


class ListControlsIndexViewMixin:
    """
    Adds filtering, sorting and other controls to a modeladmin's list/index view
    """

    _built_list_controls = None
    _items_per_page = None
    _has_prepared_list_controls = False

    def build_list_controls(self):
        """
        A hook provided to declare the filters for the UI
        """
        return ListControls()

    def apply_list_controls_to_queryset(self, queryset):
        """
        A hook provided to modify the queryset
        """
        for obj in self.get_list_controls().flatten_tree():
            if hasattr(obj, 'apply_to_queryset'):
                queryset = obj.apply_to_queryset(queryset)
        return queryset

    def get_list_controls(self):
        if not self._built_list_controls:
            list_controls = self.build_list_controls()
            # Allow the controls to be defined in a list
            if isinstance(list_controls, Iterable):
                list_controls = ListControls()(*list_controls)
            self._built_list_controls = list_controls
        return self._built_list_controls

    def get_selected_list_control_layout(self):
        for obj in self.get_list_controls().flatten_tree():
            if isinstance(obj, LayoutSelector) and obj.is_selected:
                return obj

    def get_template_names(self):
        return ['admin_list_controls/index.html'] + super().get_template_names()

    def get_filters_params(self, params=None):
        """
        Prevent the modeladmin's built-in querying from raising errors when it encounters
        our custom GET data
        """
        params = super().get_filters_params(params)

        for obj in self.get_list_controls().flatten_tree():
            name = getattr(obj, 'name', None)
            if name and name in params:
                del params[name]
        return params

    def get_search_results(self, *args, **kwargs):
        queryset = super().get_search_results(*args, **kwargs)

        self.prepare_list_controls()
        return self.apply_list_controls_to_queryset(queryset)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        selected_layout = self.get_selected_list_control_layout()
        if selected_layout and selected_layout.template:
            selected_layout_template = selected_layout.template
        else:
            selected_layout_template = None

        context_data['admin_list_controls'] = {
            'index_template': self.get_list_controls_index_template(),
            # Consumed by the front-end code to build the UI
            'initial_state': json.dumps({
                'admin_list_controls': self.get_list_controls().serialize(),
            }),
            'selected_layout_template': selected_layout_template,
            'widget_js': self.get_list_controls_widget_js(),
        }

        return context_data

    def get_list_controls_index_template(self):
        return 'modeladmin/index.html'

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

    def prepare_list_controls(self):
        # The lifecycle hooks we use to wire into the request/response are sometimes
        # executed multiple times per-request. To avoid odd bugs (components wrapping
        # other components multiple times, etc), we need to manually enforce a single
        # execution of the following method
        if self._has_prepared_list_controls:
            return
        self._has_prepared_list_controls = True

        list_controls = self.get_list_controls()

        controls_by_name = {}
        for obj in list_controls.flatten_tree():
            # Allow objects
            if hasattr(obj, 'handle_request'):
                obj.handle_request(self.request)
            name = getattr(obj, 'name', None)
            if name:
                if name not in controls_by_name:
                    controls_by_name[name] = []
                controls_by_name[name].append(obj)

        # If no selectors have been selected for a particular param,
        # indicate the default selectors should be used
        for name, controls in controls_by_name.items():
            selector_controls = [
                control for control in controls
                if control.object_type == 'selector'
            ]
            has_selected = False
            for control in selector_controls:
                if control.object_type == 'selector' and control.is_selected:
                    has_selected = True
                    break
            if not has_selected:
                for control in selector_controls:
                    if control.is_default:
                        control.is_selected = True
                        break

        # Some objects wrap their children in other components
        for obj in list_controls.flatten_tree():
            if hasattr(obj, 'prepare_children'):
                obj.prepare_children()

        # Some objects are derived from the final state of the tree

        flattened_tree = list_controls.flatten_tree()
        for obj in flattened_tree:
            if hasattr(obj, 'derive_from_components'):
                obj.derive_from_components(flattened_tree)


class ListControlsIndexView(ListControlsIndexViewMixin, IndexView):
    pass
