from .actions import SetValue, RemoveValue, SubmitForm
from .components import BaseComponent, Button, Text


class BaseSelector(BaseComponent):
    object_type = 'selector'
    selector_type = ''
    name = None
    cleaned_value = None
    summary_label = None
    summary_value = None

    def __init__(
        self,
        name,
        value,
        is_default=False,
        summary_label=None,
        summary_value=None,
        apply_to_queryset=None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.value = value
        self.is_default = is_default
        self.name = name
        self.is_selected = False
        self.summary_label = summary_label
        self.summary_value = summary_value
        self._apply_to_queryset = apply_to_queryset

    def handle_request(self, request):
        self.cleaned_value = self.clean(request)
        self.is_selected = self.cleaned_value == self.value

    def clean(self, request):
        return request.GET.get(self.name)

    def serialize(self):
        return dict(super().serialize(), **{
            'selector_type': self.selector_type,
            'name': self.name,
            'value': self.value,
            'is_default': self.is_default,
            'is_selected': self.is_selected,
        })

    def apply_to_queryset(self, queryset):
        if self._apply_to_queryset and self.is_selected:
            return self._apply_to_queryset(queryset)
        return queryset

    def prepare_children(self):
        self._original_children = self.children

        extra_classes = self.extra_classes
        if self.is_selected:
            extra_classes += ' alc__selector alc__selector--%s is-selected' % self.selector_type

        actions = []
        if self.is_selected:
            actions.append(RemoveValue(name=self.name, value=self.value))
        else:
            actions.append(SetValue(name=self.name, value=self.value))
        actions.append(SubmitForm())

        self.children = [
            Button(action=actions, extra_classes=extra_classes, style=self.style)(
                *self._original_children,
            ),
        ]

    def serialize_summary(self):
        if self.is_selected and not self.is_default:
            label = self.summary_label
            if not label:
                label = self.name.title()

            value = self.summary_value
            if value is None:
                value = ''
                for component in self.flatten_tree():
                    if isinstance(component, str):
                        value += component + ' '
                    elif isinstance(component, Text):
                        value += component.content + ' '
                value = value.strip()
                if not value:
                    value = self.cleaned_value

            return {
                'name': self.name,
                'label': label,
                'value': value,
                'action': [
                    RemoveValue(name=self.name, value=self.cleaned_value).serialize(),
                    SubmitForm().serialize(),
                ],
            }


class LayoutSelector(BaseSelector):
    selector_type = 'layout'
    DEFAULT_NAME = 'layout'

    def __init__(
        self,
        value,
        template=None,
        is_default=False,
        name=DEFAULT_NAME,
        summary_label='Layout',
        summary_value=None,
        **kwargs,
    ):
        super().__init__(
            name=name,
            value=value,
            is_default=is_default,
            summary_label=summary_label,
            summary_value=summary_value,
            **kwargs,
        )

        self.template = template


class SortSelector(BaseSelector):
    selector_type = 'sort'
    DEFAULT_NAME = 'sort'

    def __init__(
        self,
        value,
        apply_to_queryset=None,
        is_default=False,
        name=DEFAULT_NAME,
        summary_label='Sort',
        summary_value=None,
        **kwargs,
    ):
        super().__init__(
            name=name,
            value=value,
            is_default=is_default,
            summary_label=summary_label,
            summary_value=summary_value,
            **kwargs,
        )

        self._apply_to_queryset = apply_to_queryset
