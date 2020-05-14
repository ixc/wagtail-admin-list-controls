from collections.abc import Iterable
from django.utils.translation import gettext as _

from .actions import SubmitForm, ClearSearchInput
from .exceptions import ConfigurationError


class BaseComponent:
    object_type = ''
    children = None
    can_have_children = True
    _children_defined = False

    def __init__(self, style=None, extra_classes=''):
        self.style = self.get_default_style()
        if style:
            self.style.update(style)
        self.extra_classes = extra_classes
        self.component_id = '%s-%s' % (type(self).__name__, id(self))

    def __call__(self, *args):
        return self.set_children(*args)

    def set_children(self, *args):
        if self._children_defined:
            raise ConfigurationError('Children have already been defined')
        if not self.can_have_children:
            raise ConfigurationError('%s cannot have children' % type(self))
        self._children_defined = True
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

    def flatten_tree(self):
        components = [self]
        if self.children:
            for child in self.children:
                if isinstance(child, Iterable):
                    for nested_child in child:
                        components += nested_child.flatten_tree()
                else:
                    components += child.flatten_tree()
        return components


class ListControls(BaseComponent):
    object_type = 'list_controls'


class Block(BaseComponent):
    object_type = 'block'


class Spacer(Block):
    def get_default_style(self):
        return {'padding-top': '20px'}


class Columns(BaseComponent):
    object_type = 'columns'

    def __init__(self, column_count=2, **kwargs):
        super().__init__(**kwargs)
        self.column_count = column_count

    def prepare_children(self):
        self._original_children = self.children

        column_count = self.column_count
        gutter_width = '20px'
        column_width = 'calc((100% - (({cc} - 1) * {gw})) / {cc})'.format(
            cc=column_count,
            gw=gutter_width,

        )

        columns = [[] for _ in range(column_count)]
        next_column_index = 0
        for i, child in enumerate(self.children):
            next_column = columns[next_column_index]
            next_column.append(child)
            next_column_index += 1
            if (next_column_index + 1) > column_count:
                next_column_index = 0

        self.children = []
        for column_index, column_children in enumerate(columns):
            style = {
                'width': column_width,
                'float': 'left',
                'margin-left': gutter_width if column_index > 0 else '0',
            }
            self.children.append(
                Block(style)(*column_children),
            )


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


class Summary(BaseComponent):
    object_type = 'summary'

    def __init__(
        self,
        reset_label=_('Reset all'),
        include_search_query=True,
        search_query_name='q',
        search_query_label=_('Search'),
        search_query_value=None,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.reset_label = reset_label
        self.summary = []
        self.include_search_query = include_search_query
        self.search_query_name = search_query_name
        self.search_query_label = search_query_label
        self.search_query_value = search_query_value

    def handle_request(self, request):
        if self.include_search_query:
            self.search_query_value = request.GET.get(self.search_query_name)

    def derive_from_components(self, components):
        # Include the content of the built-in search field
        if self.include_search_query and self.search_query_value:
            self.summary.append({
                'name': self.search_query_name,
                'label': self.search_query_label,
                'value': self.search_query_value,
                'action': [
                    ClearSearchInput().serialize(),
                    SubmitForm().serialize(),
                ]
            })

        for component in components:
            if hasattr(component, 'serialize_summary'):
                summaries = component.serialize_summary()
                if isinstance(summaries, dict):
                    summaries = [summaries]
                if summaries:
                    self.summary += summaries

    def serialize(self):
        return dict(super().serialize(), **{
            'summary': self.summary,
            'reset_label': self.reset_label,
        })


