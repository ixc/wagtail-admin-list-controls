import os
import json
from django.conf import settings
from django.utils.safestring import mark_safe
from .options import SORT_PARAM, LAYOUT_PARAM, ListViewControls
from .vendor import webpack_manifest


class AdminListControlsMixin:
    """
    Adds filtering, sorting and other controls to a modeladmin's list/index view
    """

    _built_list_controls = None
    _items_per_page = None

    def build_list_controls(self):
        """
        A hook provided to declare the filters for the UI
        """
        return ListViewControls()

    def apply_list_controls_to_queryset(self, queryset):
        """
        A hook provided to modify the queryset
        """
        return queryset

    def get_list_controls(self):
        if not self._built_list_controls:
            self._built_list_controls = self.build_list_controls()
        return self._built_list_controls

    def get_template_names(self):
        return ['admin_list_controls/admin_list_controls.html']

    def get_selected_list_control_filters(self):
        options = self.get_list_controls()
        filters = []
        for obj in options.traverse():
            if obj.object_type == 'filter' and obj.value:
                filters.append(obj)
        return filters

    def get_selected_list_control_sorts(self):
        options = self.get_list_controls()
        if not options['sorts']:
            return []

        sorts = get_sorts_from_options(options['sorts'])
        return [
            obj for obj in sorts if obj['is_selected']
        ]

    def get_selected_list_control_layout(self):
        options = self.get_list_controls()
        if not options['layouts']:
            return

        layouts = get_layouts_from_options(options['layouts'])
        selected_layouts = [
            obj for obj in layouts if obj['is_selected']
        ]
        if selected_layouts:
            return selected_layouts[0]

    def get_filters_params(self, params=None):
        """
        Prevent the modeladmin's built-in querying from raising errors when it encounters
        our custom GET data
        """
        params = super().get_filters_params(params)
        # for obj in self.get_list_controls().traverse():
        #     if obj.name:
        #         del params[obj.name]
        return params

    def show_list_controls_reset(self):
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
        context_data.update(
            self.get_list_controls_context_data()
        )
        return context_data

    def get_list_controls_context_data(self, **kwargs):
        context_data = {}

        controls = self.get_list_controls()

        # Consumed by the front-end code to build the UI
        # context_data['admin_list_controls_initial_state'] = json.dumps({
        #     'filtering_options': options['filters'],
        #     'sorting_options': options['sorts'],
        #     'layout_options': options['layouts'],
        #     'show_reset_button': self.show_list_controls_reset(),
        #     'description': self.get_textual_description_of_controls(),
        #     'verbose_name': str(self.model._meta.verbose_name),
        #     'verbose_name_plural': str(self.model._meta.verbose_name_plural),
        # })

        # The selected layout can control which results template is rendered
        # context_data['admin_list_controls_selected_layout'] = self.get_selected_list_control_layout()

        # Initialisation for the controls UI

        context_data['admin_list_controls'] = {
            'DEBUG': settings.DEBUG,
        }

        context_data['admin_list_controls_widget_js'] = self.get_list_controls_widget_js()

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

    def get_selected_list_controls(self):
        options = self.get_list_controls()

        if options['filters']:
            filters = get_filters_from_options(options['filters'])
            filters_with_values = [
                obj for obj in filters if obj['value']
            ]
        else:
            filters_with_values = []

        if options['sorts']:
            sorts = get_sorts_from_options(options['sorts'])
            selected_sorts = [
                obj for obj in sorts if obj['is_selected']
            ]
        else:
            selected_sorts = []

        return {
            'filters': filters_with_values,
            'sorts': selected_sorts,
        }
