from django.test import RequestFactory
from django_webtest import WebTest
from admin_list_controls.base_controls import BaseFilter, BaseToggle
from admin_list_controls.controls import TextFilter, BooleanFilter, ChoiceFilter, \
    MultipleChoiceFilter, RadioFilter, Sort, Layout, ListControls, FilterPanel, \
    FilterGroup, SortPanel, LayoutControls


class TestControls(WebTest):
    def setUp(self):
        self.factory = RequestFactory()

    def test_base_filter(self):
        filter_ = BaseFilter(
            name='test_name',
            label='test_label',
        )
        filter_.prepare(self.factory.get('/?test_name=test_value'))
        self.assertEqual(filter_.cleaned_value, 'test_value')
        self.assertEqual(
            filter_.serialize(),
            {
                'object_type': 'filter',
                'children': [],
                'filter_type': '',
                'name': 'test_name',
                'label': 'test_label',
                'value': 'test_value',
            },
        )

    def test_base_filter_with_default_value(self):
        filter_ = BaseFilter(
            name='test_name',
            label='test_label',
            default_value='test_default_value',
        )
        filter_.prepare(self.factory.get('/'))
        self.assertEqual(filter_.cleaned_value, 'test_default_value')
        filter_.prepare(self.factory.get('/?test_name'))
        self.assertEqual(filter_.cleaned_value, '')
        filter_.prepare(self.factory.get('/?test_name=test_value'))
        self.assertEqual(filter_.cleaned_value, 'test_value')

    def test_text_filter_value(self):
        filter_ = TextFilter(
            name='test_name',
            label='test_label',
        )
        filter_.prepare(self.factory.get('/'))
        self.assertEqual(filter_.cleaned_value, '')
        filter_.prepare(self.factory.get('/?test_name='))
        self.assertEqual(filter_.cleaned_value, '')
        filter_.prepare(self.factory.get('/?test_name=test_value'))
        self.assertEqual(filter_.cleaned_value, 'test_value')

    def test_boolean_filter_value(self):
        filter_ = BooleanFilter(
            name='test_name',
            label='test_label',
        )
        filter_.prepare(self.factory.get('/'))
        self.assertEqual(filter_.cleaned_value, False)
        filter_.prepare(self.factory.get('/?test_name='))
        self.assertEqual(filter_.cleaned_value, False)
        filter_.prepare(self.factory.get('/?test_name=something'))
        self.assertEqual(filter_.cleaned_value, True)

    def test_radio_filter_value(self):
        filter_ = RadioFilter(
            name='test_name',
            label='test_label',
            choices=(
                ('foo', 'Foo'),
                ('bar', 'Bar'),
            )
        )
        filter_.prepare(self.factory.get('/'))
        self.assertEqual(filter_.cleaned_value, None)
        filter_.prepare(self.factory.get('/?test_name='))
        self.assertEqual(filter_.cleaned_value, None)
        filter_.prepare(self.factory.get('/?test_name=woz'))
        self.assertEqual(filter_.cleaned_value, None)
        filter_.prepare(self.factory.get('/?test_name=foo'))
        self.assertEqual(filter_.cleaned_value, 'foo')

    def test_choice_filter_value(self):
        filter_ = ChoiceFilter(
            name='test_name',
            label='test_label',
            choices=(
                ('foo', 'Foo'),
                ('bar', 'Bar'),
            )
        )
        filter_.prepare(self.factory.get('/'))
        self.assertEqual(filter_.cleaned_value, None)
        filter_.prepare(self.factory.get('/?test_name='))
        self.assertEqual(filter_.cleaned_value, None)
        filter_.prepare(self.factory.get('/?test_name=woz'))
        self.assertEqual(filter_.cleaned_value, None)
        filter_.prepare(self.factory.get('/?test_name=foo'))
        self.assertEqual(filter_.cleaned_value, 'foo')

    def test_multiple_choice_filter_value(self):
        filter_ = MultipleChoiceFilter(
            name='test_name',
            label='test_label',
            choices=(
                ('foo', 'Foo'),
                ('bar', 'Bar'),
            )
        )
        filter_.prepare(self.factory.get('/'))
        self.assertEqual(filter_.cleaned_value, [])
        filter_.prepare(self.factory.get('/?test_name='))
        self.assertEqual(filter_.cleaned_value, [])
        filter_.prepare(self.factory.get('/?test_name=woz'))
        self.assertEqual(filter_.cleaned_value, [])
        filter_.prepare(self.factory.get('/?test_name=foo'))
        self.assertEqual(filter_.cleaned_value, ['foo'])
        filter_.prepare(self.factory.get('/?test_name=foo&test_name=foo'))
        self.assertEqual(filter_.cleaned_value, ['foo', 'foo'])
        filter_.prepare(self.factory.get('/?test_name=foo&test_name=bar'))
        self.assertEqual(filter_.cleaned_value, ['foo', 'bar'])
        filter_.prepare(self.factory.get('/?test_name=foo&test_name=bar&test_name=woz'))
        self.assertEqual(filter_.cleaned_value, ['foo', 'bar'])

    def test_base_toggle(self):
        toggle = BaseToggle(
            name='test_name',
            value='test_value',
        )
        toggle.prepare(self.factory.get('/'))
        self.assertEqual(toggle.cleaned_value, None)
        self.assertEqual(toggle.is_selected, False)
        self.assertEqual(
            toggle.serialize(),
            {
                'object_type': '',
                'children': [],
                'name': 'test_name',
                'value': 'test_value',
                'is_selected': False,
            },
        )
        toggle.prepare(self.factory.get('/?test_name'))
        self.assertEqual(toggle.cleaned_value, '')
        self.assertEqual(toggle.is_selected, False)
        toggle.prepare(self.factory.get('/?test_name=random_value'))
        self.assertEqual(toggle.cleaned_value, 'random_value')
        self.assertEqual(toggle.is_selected, False)
        toggle.prepare(self.factory.get('/?test_name=test_value'))
        self.assertEqual(toggle.cleaned_value, 'test_value')
        self.assertEqual(toggle.is_selected, True)

    def test_sort(self):
        sort = Sort(
            label='test_label',
            value='test_value',
        )
        self.assertEqual(
            sort.serialize(),
            {
                'object_type': 'sort',
                'children': [],
                'name': 'sort',
                'value': 'test_value',
                'is_selected': False,
                'label': 'test_label',
            },
        )

        sort = Sort(
            label='test_label',
            value='test_value',
            name='test_name',
        )
        self.assertEqual(
            sort.serialize(),
            {
                'object_type': 'sort',
                'children': [],
                'name': 'test_name',
                'value': 'test_value',
                'is_selected': False,
                'label': 'test_label',
            },
        )

    def test_sort_value(self):
        sort = Sort(
            label='test_label',
            value='test_value',
        )
        sort.prepare(self.factory.get('/'))
        self.assertEqual(sort.cleaned_value, None)
        self.assertEqual(sort.is_selected, False)
        self.assertEqual(sort.serialize()['label'], 'test_label')
        sort.prepare(self.factory.get('/?sort'))
        self.assertEqual(sort.cleaned_value, '')
        self.assertEqual(sort.is_selected, False)
        sort.prepare(self.factory.get('/?sort=random_value'))
        self.assertEqual(sort.cleaned_value, 'random_value')
        self.assertEqual(sort.is_selected, False)
        sort.prepare(self.factory.get('/?sort=test_value'))
        self.assertEqual(sort.cleaned_value, 'test_value')
        self.assertEqual(sort.is_selected, True)

    def test_layout(self):
        layout = Layout(
            label='test_label',
            value='test_value',
        )
        self.assertEqual(
            layout.serialize(),
            {
                'object_type': 'layout',
                'children': [],
                'name': 'layout',
                'value': 'test_value',
                'is_selected': False,
                'label': 'test_label',
                'icon_class': None,
            },
        )

        layout = Layout(
            label='test_label',
            value='test_value',
            name='test_name',
            icon_class='test_icon_class',
            template='test_template',
        )
        self.assertEqual(
            layout.serialize(),
            {
                'object_type': 'layout',
                'children': [],
                'name': 'test_name',
                'value': 'test_value',
                'is_selected': False,
                'label': 'test_label',
                'icon_class': 'test_icon_class',
            },
        )

    def test_layout_value(self):
        layout = Layout(
            label='test_label',
            value='test_value',
        )
        layout.prepare(self.factory.get('/'))
        self.assertEqual(layout.cleaned_value, None)
        self.assertEqual(layout.is_selected, False)
        self.assertEqual(layout.serialize()['label'], 'test_label')
        layout.prepare(self.factory.get('/?layout'))
        self.assertEqual(layout.cleaned_value, '')
        self.assertEqual(layout.is_selected, False)
        layout.prepare(self.factory.get('/?layout=random_value'))
        self.assertEqual(layout.cleaned_value, 'random_value')
        self.assertEqual(layout.is_selected, False)
        layout.prepare(self.factory.get('/?layout=test_value'))
        self.assertEqual(layout.cleaned_value, 'test_value')
        self.assertEqual(layout.is_selected, True)

    def test_list_controls_serialization(self):
        self.assertEqual(
            ListControls([]).serialize(),
            {
                'object_type': 'list_controls',
                'children': [],
            }
        )

    def test_filter_panel_serialization(self):
        self.assertEqual(
            FilterPanel([]).serialize(),
            {
                'object_type': 'filter_panel',
                'children': [],
                'label': 'Filters',
            }
        )
        self.assertEqual(
            FilterPanel([], label='test_label').serialize(),
            {
                'object_type': 'filter_panel',
                'children': [],
                'label': 'test_label',
            }
        )

    def test_filter_group_serialization(self):
        self.assertEqual(
            FilterGroup([]).serialize(),
            {
                'object_type': 'filter_group',
                'children': [],
                'label': None,
            }
        )
        self.assertEqual(
            FilterGroup([], label='test_label').serialize(),
            {
                'object_type': 'filter_group',
                'children': [],
                'label': 'test_label',
            }
        )

    def test_sort_panel_serialization(self):
        self.assertEqual(
            SortPanel([]).serialize(),
            {
                'object_type': 'sort_panel',
                'children': [],
                'label': 'Order results',
            }
        )
        self.assertEqual(
            SortPanel([], label='test_label').serialize(),
            {
                'object_type': 'sort_panel',
                'children': [],
                'label': 'test_label',
            }
        )

    def test_layout_controls_serialization(self):
        self.assertEqual(
            LayoutControls([]).serialize(),
            {
                'object_type': 'layout_controls',
                'children': [],
            }
        )

    def test_nested_serialization(self):
        self.assertEqual(
            ListControls([
                ListControls([
                    ListControls([]),
                ]),
                ListControls([
                    ListControls([]),
                ])
            ]).serialize(),
            {
                'object_type': 'list_controls',
                'children': [{
                    'object_type': 'list_controls',
                    'children': [{
                        'object_type': 'list_controls',
                        'children': [],
                    }],
                }, {
                    'object_type': 'list_controls',
                    'children': [{
                        'object_type': 'list_controls',
                        'children': [],
                    }],
                }],
            }
        )
