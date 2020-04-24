import os
import json
from django.conf import settings
from django.utils.safestring import mark_safe
from wagtail.contrib.modeladmin.views import IndexView
from .base_controls import BaseFilter
from .controls import ListControls, Sort, Layout
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

    def get_list_control_filters(self):
        objects = []
        for obj in self.get_list_controls().flatten_hierarchy():
            if obj.object_type == BaseFilter.object_type:
                objects.append(obj)
        return objects

    def get_list_control_sorts(self):
        objects = []
        for obj in self.get_list_controls().flatten_hierarchy():
            if obj.object_type == Sort.object_type:
                objects.append(obj)
        return objects

    def get_list_control_layouts(self):
        objects = []
        for obj in self.get_list_controls().flatten_hierarchy():
            if obj.object_type == Layout.object_type:
                objects.append(obj)
        return objects

    def get_template_names(self):
        return ['admin_list_controls/admin_list_controls.html']

    def get_selected_list_control_filters(self):
        selected_filters = []
        for filter_ in self.get_list_control_filters():
            if filter_.value:
                selected_filters.append(filter_)
        return selected_filters

    def get_selected_list_control_sort(self):
        for sort in self.get_list_control_sorts():
            if sort.is_selected:
                return sort

    def get_selected_list_control_layout(self):
        for layout in self.get_list_control_layouts():
            if layout.is_selected:
                return layout

    def get_filters_params(self, params=None):
        """
        Prevent the modeladmin's built-in querying from raising errors when it encounters
        our custom GET data
        """
        params = super().get_filters_params(params)

        controls_with_params = (
            self.get_list_control_filters()
            + self.get_list_control_sorts()
            + self.get_list_control_layouts()
        )
        for obj in controls_with_params:
            if obj.name in params:
                del params[obj.name]
        return params

    def show_admin_list_controls_reset(self):
        for filter in self.get_selected_list_control_filters():
            if not filter['is_default']:
                return True
        for sort in self.get_selected_list_control_sorts():
            if not sort['is_default']:
                return True
        return False

    def get_search_results(self, *args, **kwargs):
        queryset = super().get_search_results(*args, **kwargs)
        queryset = self.apply_list_controls_to_queryset(queryset)
        return queryset

    def get_textual_description_of_controls(self):
        """
        Produces a textual representation of the applied filtering and sorting.
        """
        selected_filters = self.get_selected_list_control_filters()
        selected_sorts = self.get_selected_list_control_sorts()

        description_parts = []
        if self.query:
            description_parts.append(' matching <strong>%s</strong>' % self.query)
        if selected_filters:
            description_parts += [
                obj['results_description']
                for obj in selected_filters
                # Allow suppression of a filter in the description
                if obj['results_description'] is not None
            ]

        description = ''
        if description_parts:
            description += 'Filters: '
            if len(description_parts) == 1:
                description += description_parts[0]
            elif len(description_parts) == 2:
                description += ' and '.join(description_parts)
            elif len(description_parts) >= 3:
                description += ', '.join(description_parts[:-1])
                description += ' and %s' % description_parts[-1]
            description += '. '

        if selected_sorts:
            if len(selected_sorts) == 1 and selected_sorts[0].get('is_default'):
                # When the default sort is applied, don't output any indication of it
                pass
            else:
                description += '. '.join(
                    [sort_obj['results_description'] for sort_obj in selected_sorts]
                )
                description += '. '

        return description

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        # Consumed by the front-end code to build the UI
        context_data['admin_list_controls'] = {
            'initial_state': json.dumps({
                'admin_list_controls': self.get_list_controls().serialize(),
                # 'show_reset_button': self.show_admin_list_controls_reset(),
                # 'description': self.get_textual_description_of_controls(),
                # 'verbose_name': str(self.model._meta.verbose_name),
                # 'verbose_name_plural': str(self.model._meta.verbose_name_plural),
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
