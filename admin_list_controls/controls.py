from django.utils.translation import gettext as _
from .base_controls import BaseControl, BaseFilter, BaseToggle


class ListControls(BaseControl):
    object_type = 'list_controls'

    def __init__(self, children, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.children = children


class Block(BaseControl):
    object_type = 'block'

    def __init__(self, width=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.width = width

    def serialize(self):
        return dict(super().serialize(), **{
            'width': self.width,
        })


class FilterPanel(BaseControl):
    object_type = 'filter_panel'
    label = _('Filters')

    def __init__(self, children, label=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.children = children
        if label:
            self.label = label

    def serialize(self):
        return dict(super().serialize(), **{
            'label': self.label,
        })


class FilterGroup(BaseControl):
    object_type = 'filter_group'

    def __init__(self, children, label=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.children = children
        self.label = label

    def serialize(self):
        return dict(super().serialize(), **{
            'label': self.label,
        })


class TextFilter(BaseFilter):
    filter_type = 'text'

    def clean(self, *args, **kwargs):
        value = super().clean(*args, **kwargs)
        if value is None:
            return ''
        return value


class BooleanFilter(BaseFilter):
    filter_type = 'boolean'

    def clean(self, *args, **kwargs):
        value = super().clean(*args, **kwargs)
        return bool(value)


class RadioFilter(BaseFilter):
    filter_type = 'radio'

    def __init__(self, choices, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.choices = choices

    def clean(self, request):
        whitelisted_values = [choice[0] for choice in self.choices]
        value = request.GET.get(self.name)
        if value in whitelisted_values:
            return value

    def serialize(self):
        return dict(super().serialize(), **{
            'choices': self.choices,
        })


class ChoiceFilter(BaseFilter):
    filter_type = 'choice'

    def __init__(self, choices, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.choices = choices

    def serialize(self):
        return dict(super().serialize(), **{
            'choices': self.choices,
        })

    def clean(self, request):
        whitelisted_values = [choice[0] for choice in self.choices]
        value = request.GET.get(self.name)
        if value in whitelisted_values:
            return value


class MultipleChoiceFilter(ChoiceFilter):
    filter_type = 'multiple_choice'

    def clean(self, request):
        whitelisted_values = [choice[0] for choice in self.choices]
        values = request.GET.getlist(self.name)
        return [
            value for value in values
            if value in whitelisted_values
        ]


class SortPanel(BaseControl):
    object_type = 'sort_panel'
    label = _('Order results')

    def __init__(self, children, label=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if label:
            self.label = label

    def serialize(self):
        return dict(super().serialize(), **{
            'label': self.label,
        })


class Sort(BaseToggle):
    object_type = 'sort'

    def __init__(self, label, name='sort', *args, **kwargs):
        super().__init__(name=name, *args, **kwargs)

        self.label = label

    def serialize(self):
        return dict(super().serialize(), **{
            'label': self.label,
            'name': self.name,
        })


class LayoutControls(BaseControl):
    object_type = 'layout_controls'

    def __init__(self, children, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.children = children


class Layout(BaseToggle):
    object_type = 'layout'

    def __init__(self, label, icon_class=None, template=None, name='layout', *args, **kwargs):
        super().__init__(name=name, *args, **kwargs)

        self.label = label
        self.icon_class = icon_class
        self.template = template

    def serialize(self):
        return dict(super().serialize(), **{
            'label': self.label,
            'icon_class': self.icon_class,
        })
