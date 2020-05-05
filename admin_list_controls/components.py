from collections.abc import Iterable


class BaseComponent:
    object_type = ''
    children = None
    _flattened_hierarchy = None

    # def __call__(self, *args):
    #     return self.set_children(*args)
    #
    # def set_children(self, *args):
    #     self.children = args
    #     return self

    def serialize(self):
        serialized_children = []
        if self.children:
            for child in self.children:
                if isinstance(child, str):
                    serialized_children.append(child)
                else:
                    serialized_children.append(child.serialize())

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


class ListControls(BaseComponent):
    object_type = 'list_controls'

    def __init__(self, children):
        self.children = children


class Block(BaseComponent):
    object_type = 'block'
    LEFT = 'left'
    RIGHT = 'right'

    def __init__(self, children, float=None):
        self.children = children
        self.float = float

    def serialize(self):
        return dict(super().serialize(), **{
            'float': self.float,
        })


class Row(BaseComponent):
    object_type = 'row'

    def __init__(self, children):
        self.children = children


class Column(BaseComponent):
    object_type = 'column'
    HALF_WIDTH = 'half_width'
    QUARTER_WIDTH = 'quarter_width'
    FULL_WIDTH = 'full_width'

    def __init__(self, children, width):
        self.children = children
        self.width = width

    def serialize(self):
        return dict(super().serialize(), **{
            'width': self.width,
        })


class Divider(BaseComponent):
    object_type = 'divider'


class Panel(BaseComponent):
    object_type = 'panel'

    def __init__(self, children, ref=None, collapsed=False):
        self.children = children
        self.ref = ref
        self.collapsed = collapsed

    def serialize(self):
        return dict(super().serialize(), **{
            'collapsed': self.collapsed,
        })


class Icon(BaseComponent):
    object_type = 'icon'

    def __init__(self, class_name):
        self.class_name = class_name

    def serialize(self):
        return dict(super().serialize(), **{
            'class_name': self.class_name,
        })


class Text(BaseComponent):
    object_type = 'text'
    LARGE = 'large'
    REGULAR = 'regular'
    SMALL = 'small'

    def __init__(self, children, size=REGULAR):
        if isinstance(children, str):
            self.children = [children]
        else:
            self.children = children
        self.size = size

    def serialize(self):
        return dict(super().serialize(), **{
            'size': self.size,
        })


class Button(BaseComponent):
    object_type = 'button'

    def __init__(self, children, action=None):
        self.children = children
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

    def __init__(self, content):
        self.content = content

    def serialize(self):
        return dict(super().serialize(), **{
            'content': self.content,
        })





