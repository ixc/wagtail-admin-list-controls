from .components import BaseComponent


class BaseFilter(BaseComponent):
    object_type = 'filter'
    filter_type = ''
    name = None
    cleaned_value = None
    can_have_children = False

    def __init__(self, name, label=None, apply_to_queryset=None, default_value=None, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.label = label
        self._apply_to_queryset = apply_to_queryset
        self.default_value = default_value

    def handle_request(self, request):
        self.cleaned_value = self.clean(request)
        if self.cleaned_value is None:
            self.cleaned_value = self.default_value

    def clean(self, request):
        return request.GET.get(self.name)

    def apply_to_queryset(self, queryset):
        if self._apply_to_queryset:
            return self._apply_to_queryset(queryset, self.cleaned_value)
        return super().apply_to_queryset(queryset)

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

    def clean(self, request):
        whitelisted_values = [choice[0] for choice in self.choices]
        value = request.GET.get(self.name)
        if value in whitelisted_values:
            return value

    def serialize(self):
        return dict(super().serialize(), **{
            'choices': self.choices,
        })


class MultipleChoiceFilter(ChoiceFilter):
    filter_type = 'multiple_choice'

    def clean(self, request):
        whitelisted_values = [choice[0] for choice in self.choices]
        values = request.GET.getlist(self.name)
        return [
            value for value in values
            if value in whitelisted_values
        ]
