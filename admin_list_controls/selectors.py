from .actions import SetValue, RemoveValue, SubmitForm
from .components import BaseComponent, Button


class BaseSelector(BaseComponent):
    object_type = 'selector'
    selector_type = ''
    name = None
    cleaned_value = None

    def __init__(self, name, value, is_default=False, **kwargs):
        super().__init__(**kwargs)
        self.value = value
        self.is_default = is_default
        self.name = name
        self.is_selected = False

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
            'is_selected': self.is_selected,
        })

    def prepare_children(self):
        self._original_children = self.children

        extra_classes = None
        if self.is_selected:
            extra_classes = 'is-selected'

        actions = []
        if self.is_selected:
            actions.append(RemoveValue(name=self.name, value=self.value))
        else:
            actions.append(SetValue(name=self.name, value=self.value))
        actions.append(SubmitForm())

        self.children = [
            Button(action=actions, extra_classes=extra_classes)(
                *self._original_children,
            ),
        ]


class Layout(BaseSelector):
    selector_type = 'layout'

    def __init__(self, value, template=None, is_default=False, name='layout', **kwargs):
        super().__init__(name=name, value=value, is_default=is_default, **kwargs)

        self.template = template
