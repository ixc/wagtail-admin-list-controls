from admin_list_controls.exceptions import ConfigurationError


class BaseControl:
    object_type = ''

    def __init__(self, children=None, *args, **kwargs):
        if children:
            self.children = children
        else:
            self.children = []

    def prepare(self, *args, **kwargs):
        pass

    def clean(self, *args, **kwargs):
        pass

    def apply_to_queryset(self, queryset):
        return queryset

    def serialize(self):
        serialized_children = []
        if self.children:
            serialized_children = [
                child.serialize() for child in self.children
            ]

        return {
            'object_type': self.object_type,
            'children': serialized_children,
        }

    def traverse(self):
        yield self
        for child in self.children:
            yield child.traverse()


class BaseDataControl(BaseControl):
    cleaned_value = None

    def __init__(self, name, apply_to_queryset=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.name = name
        if not self.name:
            raise ConfigurationError('A `name` must be provided')

        self._apply_to_queryset = apply_to_queryset

    def prepare(self, request):
        self.cleaned_value = self.clean(request)

    def clean(self, request):
        return request.GET.get(self.name)

    def serialize(self):
        return dict(super().serialize(), **{
            'name': self.name,
            'value': self.cleaned_value,
        })


class BaseToggle(BaseDataControl):
    is_selected = False

    def __init__(self, value, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.value = value

    def prepare(self, *args, **kwargs):
        super().prepare(*args, **kwargs)

        self.is_selected = self.cleaned_value == self.value

    def clean(self, request):
        return request.GET.get(self.name)

    def apply_to_queryset(self, queryset):
        if self._apply_to_queryset:
            return self._apply_to_queryset(queryset)
        return super().apply_to_queryset(queryset)

    def serialize(self):
        return dict(super().serialize(), **{
            'name': self.name,
            'value': self.value,
            'is_selected': self.is_selected,
        })


class BaseFilter(BaseDataControl):
    HALF_WIDTH = 'half_width'
    FULL_WIDTH = 'full_width'

    object_type = 'filter'
    filter_type = ''

    def __init__(self, label, width=HALF_WIDTH, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.label = label
        self.width = width

    def apply_to_queryset(self, queryset):
        if self._apply_to_queryset:
            return self._apply_to_queryset(queryset, self.cleaned_value)
        return super().apply_to_queryset(queryset)

    def serialize(self):
        return dict(super().serialize(), **{
            'filter_type': self.filter_type,
            'label': self.label,
            'width': self.width,
        })
