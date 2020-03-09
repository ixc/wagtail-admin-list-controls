STRING_FILTER = 'string'
CHOICE_FILTER = 'choice'
BOOLEAN_FILTER = 'boolean'
RADIO_FILTER = 'radio'

HALF_WIDTH_FILTER = 'half_width'
FULL_WIDTH_FILTER = 'full_width'

VALID_FILTERS = (
    STRING_FILTER,
    CHOICE_FILTER,
    BOOLEAN_FILTER,
    RADIO_FILTER,
)

VALID_FILTER_WIDTHS = (
    HALF_WIDTH_FILTER,
    FULL_WIDTH_FILTER,
)

SORT_PARAM = 'sort'
LAYOUT_PARAM = 'layout'


# These constructors are using pascal case to masquerade as classes, but they're simply
# generating dictionaries that declare the desired structure for the UI. This helps to
# reduce verbosity when declaring options, while also providing an API that'll allow us
# to add more features/validation/etc.


def ListViewOptions(filters=None, sorts=None, layouts=None):
    assert isinstance(filters, (dict, type(None)))
    assert isinstance(sorts, (dict, type(None)))
    assert isinstance(layouts, (dict, type(None)))

    return {
        'filters': filters,
        'sorts': sorts,
        'layouts': layouts,
    }


def FilterOptions(children):
    assert isinstance(children, list)

    return {
        'object_type': 'filter_options',
        'children': children,
    }


def FilterGroup(title, children):
    assert isinstance(title, str)
    assert isinstance(children, list)
    for obj in children:
        assert isinstance(obj, dict)

    return {
        'object_type': 'filter_group',
        'title': title,
        'children': children,
    }


def Filter(
    name, label, type, value, results_description, choices=None, multiple=None, clearable=None,
    width=None, is_default=None,
):
    if width is None:
        width = HALF_WIDTH_FILTER

    assert type in VALID_FILTERS
    assert width in VALID_FILTER_WIDTHS

    return {
        'object_type': 'filter',
        'name': name,
        'label': label,
        'type': type,
        'value': value,
        'results_description': results_description,
        'choices': choices,
        'multiple': multiple,
        'clearable': clearable,
        'width': width,
        'is_default': is_default,
    }


def SortOptions(children):
    assert isinstance(children, list)

    return {
        'object_type': 'sort_options',
        'children': children,
    }


def Sort(label, value, is_selected, results_description, name=None, is_default=None):
    if name is None:
        name = SORT_PARAM

    return {
        'object_type': 'sort',
        'name': name,
        'label': label,
        'value': value,
        'is_selected': is_selected,
        'results_description': results_description,
        'is_default': is_default,
    }


def LayoutOptions(children):
    assert isinstance(children, list)

    return {
        'object_type': 'layout_options',
        'children': children,
    }


def Layout(label, value, is_selected, icon_class, template=None, name=None):
    if name is None:
        name = LAYOUT_PARAM

    return {
        'object_type': 'layout',
        'name': name,
        'label': label,
        'value': value,
        'is_selected': is_selected,
        'icon_class': icon_class,
        'template': template,
    }
