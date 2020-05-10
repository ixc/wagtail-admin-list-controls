from collections.abc import Iterable
from .exceptions import ConfigurationError


class BaseComponent:
    object_type = ''
    children = None
    can_have_children = True
    _flattened_hierarchy = None
    _added_children = False

    def __init__(self, style=None, extra_classes=None):
        self.style = self.get_default_style()
        if style:
            self.style.update(style)
        self.extra_classes = extra_classes
        self.component_id = '%s-%s' % (type(self).__name__, id(self))

    def __call__(self, *args):
        return self.set_children(*args)

    def set_children(self, *args):
        if self._added_children:
            raise ConfigurationError('Children have already been defined')
        if not self.can_have_children:
            raise ConfigurationError('%s cannot have children' % type(self))
        self._added_children = True
        self.children = []
        for child in args:
            if isinstance(child, str):
                self.children.append(
                    Text(content=child))
            else:
                self.children.append(child)
        return self

    def serialize(self):
        serialized_children = None
        if self.children:
            serialized_children = [
                child.serialize()
                for child in self.children
            ]

        return {
            'component_id': self.component_id,
            'object_type': self.object_type,
            'children': serialized_children,
            'style': self.serialize_style(),
            'extra_classes': self.extra_classes,
        }

    def serialize_style(self):
        """
        Convert conventional css-props into the camel-case that React prefers
        """
        if not self.style:
            return None

        serialized = {}
        for key, value in self.style.items():
            if '-' in key:
                parts = key.split('-')
                converted = parts[0] + ''.join(part.title() for part in parts[1:])
                serialized[converted] = value
            else:
                serialized[key] = value
        return serialized

    def get_default_style(self):
        return {}

    def flatten_hierarchy(self):
        hierarchy = [self]
        if self.children:
            for child in self.children:
                hierarchy += child.flatten_hierarchy()
        return hierarchy


class ListControls(BaseComponent):
    object_type = 'list_controls'


class Block(BaseComponent):
    object_type = 'block'


class Spacer(Block):
    def get_default_style(self):
        return {'padding-top': '20px'}


class Row(BaseComponent):
    object_type = 'row'


class Column(BaseComponent):
    object_type = 'column'

    QUARTER_WIDTH = 'quarter_width'
    HALF_WIDTH = 'half_width'
    FULL_WIDTH = 'full_width'

    def __init__(self, width, **kwargs):
        super().__init__(**kwargs)
        self.width = width

    def serialize(self):
        return dict(super().serialize(), **{
            'width': self.width,
        })


class Divider(BaseComponent):
    object_type = 'divider'
    can_have_children = False


class Panel(BaseComponent):
    object_type = 'panel'

    def __init__(self, ref=None, collapsed=False, **kwargs):
        super().__init__(**kwargs)
        self.ref = ref
        self.collapsed = collapsed

    def serialize(self):
        return dict(super().serialize(), **{
            'ref': self.ref,
            'collapsed': self.collapsed,
        })


class Icon(BaseComponent):
    object_type = 'icon'
    can_have_children = False

    def __init__(self, classes=None, **kwargs):
        if classes:
            kwargs['extra_classes'] = classes
        super().__init__(**kwargs)


class Text(BaseComponent):
    object_type = 'text'
    can_have_children = False

    # Sizes
    LARGE = 'large'
    MEDIUM = 'medium'

    def __init__(self, content, size=MEDIUM, **kwargs):
        super().__init__(**kwargs)
        self.content = content
        self.size = size

    def serialize(self):
        return dict(super().serialize(), **{
            'content': self.content,
            'size': self.size,
        })


class Button(BaseComponent):
    object_type = 'button'

    def __init__(self, action=None, **kwargs):
        super().__init__(**kwargs)
        if action is None:
            action = []
        elif not isinstance(action, Iterable):
            # Allow single actions to be defined without wrapping them in a list
            action = [action]
        self.action = action

    def serialize(self):
        serialized_action = []
        for action in self.action:
            serialized_action.append(action.serialize())
        return dict(super().serialize(), **{
            'action': serialized_action,
        })


class Html(BaseComponent):
    object_type = 'html'
    can_have_children = False

    def __init__(self, content, **kwargs):
        super().__init__(**kwargs)
        self.content = content

    def serialize(self):
        return dict(super().serialize(), **{
            'content': self.content,
        })





