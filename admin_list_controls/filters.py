from .components import BaseComponent
from .actions import RemoveValue, SubmitForm


class BaseFilter(BaseComponent):
    object_type = 'filter'
    filter_type = ''
    name = None
    cleaned_value = None
    can_have_children = False

    def __init__(
        self,
        name,
        label=None,
        apply_to_queryset=None,
        default_value=None,
        summary_label=None,
        exclude_default_value_from_summary=True,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.name = name
        self.label = label
        self._apply_to_queryset = apply_to_queryset
        self.default_value = default_value
        self.summary_label = summary_label
        self.exclude_default_value_from_summary = exclude_default_value_from_summary

    def handle_request(self, request):
        self.cleaned_value = self.clean(request)
        if self.cleaned_value is None:
            self.cleaned_value = self.default_value

    def clean(self, request):
        return request.GET.get(self.name)

    def apply_to_queryset(self, queryset):
        if self._apply_to_queryset and self.cleaned_value:
            return self._apply_to_queryset(queryset, self.cleaned_value)
        return queryset

    def serialize_summary(self):
        if self.exclude_default_value_from_summary and self.cleaned_value == self.default_value:
            return
        return self.serialize_summary_for_value(self.cleaned_value)

    def serialize_summary_for_value(self, value):
        if value:
            label = self.summary_label
            if not label:
                label = self.label
            display_value = self.get_summary_display_value_for_value(value)

            return {
                'name': self.name,
                'label': label,
                'display_value': display_value,
                'value': value,
                'action': [
                    RemoveValue(name=self.name, value=value).serialize(),
                    SubmitForm().serialize(),
                ],
            }

    def get_summary_display_value_for_value(self, value):
        return value

    def serialize(self):
        return dict(super().serialize(), **{
            'filter_type': self.filter_type,
            'name': self.name,
            'label': self.label,
            'value': self.cleaned_value,
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


class BaseChoiceFilter(BaseFilter):
    def __init__(self, choices, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.choices = choices

    def clean(self, request):
        whitelisted_values = [choice[0] for choice in self.choices]
        value = request.GET.get(self.name)
        if value in whitelisted_values:
            return value
        elif self.default_value:
            return self.default_value

    def serialize(self):
        return dict(super().serialize(), **{
            'choices': self.choices,
        })

    def get_summary_display_value_for_value(self, value):
        """
        Returns the corresponding display value for the raw value
        """
        choice_dict = dict(self.choices)
        return choice_dict.get(value, value)


class RadioFilter(BaseChoiceFilter):
    filter_type = 'radio'


class ChoiceFilter(BaseChoiceFilter):
    filter_type = 'choice'

    def __init__(self, choices, multiple=False, *args, **kwargs):
        super().__init__(choices=choices, *args, **kwargs)

        self.multiple = multiple

    def clean(self, request):
        if self.multiple:
            whitelisted_values = [choice[0] for choice in self.choices]
            values = request.GET.getlist(self.name)
            cleaned_values = [
                value for value in values
                if value in whitelisted_values
            ]
            if cleaned_values:
                return cleaned_values
            elif self.default_value:
                return [self.default_value]
            else:
                return []
        return super().clean(request)

    def serialize_summary(self):
        if self.multiple:
            summaries = []
            for value in self.cleaned_value:
                summaries.append(
                    self.serialize_summary_for_value(value))
            return summaries
        return super().serialize_summary()

    def serialize(self):
        return dict(super().serialize(), **{
            'multiple': self.multiple,
        })
