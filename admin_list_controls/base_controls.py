class BaseControl:
    object_type = ''
    children = None

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

    def flatten_hierarchy(self):
        hierarchy = [self]
        if self.children:
            for child in self.children:
                hierarchy += child.flatten_hierarchy()
        return hierarchy


class BaseDataControl(BaseControl):
    cleaned_value = None

    def __init__(self, name, apply_to_queryset=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.name = name
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

    def __init__(self, label=None, width=HALF_WIDTH, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if label:
            self.label = label
        else:
            self.label = self.name
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
