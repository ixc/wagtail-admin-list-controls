HALF_WIDTH_FILTER = 'half_width'
FULL_WIDTH_FILTER = 'full_width'

VALID_FILTER_WIDTHS = (
    HALF_WIDTH_FILTER,
    FULL_WIDTH_FILTER,
)

SORT_PARAM = 'sort'
LAYOUT_PARAM = 'layout'


class BaseListControl:
    object_type = ''

    def __init__(self, children=None, *args, **kwargs):
        assert self.object_type
        if children:
            self.children = children
        else:
            self.children = []

    def serialize(self):
        return {
            'object_type': self.object_type,
            'children': [
                child.serialize() for child in self.children
            ]
        }

    def traverse(self):
        yield self
        for child in self.children:
            yield child.traverse()


class ListViewControls(BaseListControl):
    object_type = 'list_view_controls'


class FilterPanel(BaseListControl):
    object_type = 'filter_panel'


class FilterGroup(BaseListControl):
    object_type = 'filter_group'

    def __init__(self, title, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title = title

    def serialize(self):
        serialized = super().serialize()
        serialized.update({
            'title': self.title,
        })
        return serialized


class BaseFilter(BaseListControl):
    object_type = 'filter'
    filter_type = ''

    def __init__(self, name, label, value, results_description, is_default=None, width=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        assert self.filter_type
        self.name = name
        self.label = label
        self.value = value
        self.results_description = results_description
        self.is_default = is_default
        if width:
            assert width in VALID_FILTER_WIDTHS
            self.width = width
        else:
            self.width = HALF_WIDTH_FILTER

    def serialize(self):
        serialized = super().serialize()
        serialized.update({
            'type': self.type,
            'name': self.name,
            'label': self.label,
            'value': self.value,
            'results_description': self.results_description,
            'is_default': self.is_default,
            'width': self.width,
        })
        return serialized


class StringFilter(BaseFilter):
    filter_type = 'string'


class BooleanFilter(BaseFilter):
    filter_type = 'boolean'


class RadioFilter(BaseFilter):
    filter_type = 'radio'

    def __init__(self, choices, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.choices = choices

    def serialize(self):
        serialized = super().serialize()
        serialized.update({
            'choices': self.choices,
        })
        return serialized


class ChoiceFilter(BaseFilter):
    filter_type = 'choice'

    def __init__(self, choices, multiple=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.choices = choices
        self.multiple = multiple

    def serialize(self):
        serialized = super().serialize()
        serialized.update({
            'choices': self.choices,
            'multiple': self.multiple,
        })
        return serialized


class SortPanel(BaseListControl):
    object_type = 'sort_panel'


class Sort(BaseListControl):
    object_type = 'sort'

    def __init__(self, label, value, is_selected, results_description, name=None, is_default=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.label = label
        self.value = value
        self.is_selected = is_selected
        self.results_description = results_description
        if name:
            self.name = name
        else:
            self.name = SORT_PARAM
        self.is_default = is_default

    def serialize(self):
        serialized = super().serialize()
        serialized.update({
            'label': self.label,
            'value': self.value,
            'is_selected': self.is_selected,
            'results_description': self.results_description,
            'name': self.name,
            'is_default': self.is_default,
        })
        return serialized


class LayoutOptions(BaseListControl):
    object_type = 'layout_options'


class Layout(BaseListControl):
    object_type = 'layout'

    def __init__(self, label, value, is_selected, icon_class, template=None, name=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.label = label
        self.value = value
        self.is_selected = is_selected
        self.icon_class = icon_class
        self.template = template
        if name:
            self.name = name
        else:
            self.name = LAYOUT_PARAM

    def serialize(self):
        serialized = super().serialize()
        serialized.update({
            'label': self.label,
            'value': self.value,
            'is_selected': self.is_selected,
            'icon_class': self.icon_class,
            'template': self.template,
            'name': self.name,
        })
        return serialized
