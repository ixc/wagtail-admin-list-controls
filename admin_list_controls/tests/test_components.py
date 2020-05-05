from django.test import TestCase
from admin_list_controls.components import ListControls, Block, Row, Column, Divider, Panel, \
    Icon, Text, Button, Html


class TestComponents(TestCase):
    def test_list_controls_component(self):
        self.assertEqual(
            ListControls([]).serialize(),
            {
                'object_type': 'list_controls',
                'children': [],
            },
        )

    def test_block_component(self):
        self.assertEqual(
            Block([]).serialize(),
            {
                'object_type': 'block',
                'children': [],
                'float': None,
            },
        )
        self.assertEqual(
            Block([], float=Block.LEFT).serialize(),
            {
                'object_type': 'block',
                'children': [],
                'float': 'left',
            },
        )
        self.assertEqual(
            Block([], float=Block.RIGHT).serialize(),
            {
                'object_type': 'block',
                'children': [],
                'float': 'right',
            },
        )

    def test_row_component(self):
        self.assertEqual(
            Row([]).serialize(),
            {
                'object_type': 'row',
                'children': [],
            },
        )

    def test_column_component(self):
        self.assertEqual(
            Column([], width=Column.HALF_WIDTH).serialize(),
            {
                'object_type': 'column',
                'children': [],
                'width': 'half_width',
            },
        )
        self.assertEqual(
            Column([], width=Column.QUARTER_WIDTH).serialize(),
            {
                'object_type': 'column',
                'children': [],
                'width': 'quarter_width',
            },
        )
        self.assertEqual(
            Column([], width=Column.FULL_WIDTH).serialize(),
            {
                'object_type': 'column',
                'children': [],
                'width': 'full_width',
            },
        )

    def test_divider_component(self):
        self.assertEqual(
            Divider().serialize(),
            {
                'object_type': 'divider',
                'children': [],
            },
        )

    def test_panel_component(self):
        self.assertEqual(
            Panel([]).serialize(),
            {
                'object_type': 'panel',
                'children': [],
                'collapsed': False,
            },
        )
        self.assertEqual(
            Panel([], collapsed=True).serialize(),
            {
                'object_type': 'panel',
                'children': [],
                'collapsed': True,
            },
        )
        self.assertEqual(
            Panel([], collapsed=False).serialize(),
            {
                'object_type': 'panel',
                'children': [],
                'collapsed': False,
            },
        )

    def test_icon_component(self):
        self.assertEqual(
            Icon(class_name='test_class_name').serialize(),
            {
                'object_type': 'icon',
                'children': [],
                'class_name': 'test_class_name',
            },
        )

    def test_text_component(self):
        self.assertEqual(
            Text([]).serialize(),
            {
                'object_type': 'text',
                'children': [],
                'size': 'regular',
            },
        )
        self.assertEqual(
            Text('test').serialize(),
            {
                'object_type': 'text',
                'children': ['test'],
                'size': 'regular',
            },
        )
        self.assertEqual(
            Text('test', size=Text.SMALL).serialize(),
            {
                'object_type': 'text',
                'children': ['test'],
                'size': 'small',
            },
        )
        self.assertEqual(
            Text('test', size=Text.REGULAR).serialize(),
            {
                'object_type': 'text',
                'children': ['test'],
                'size': 'regular',
            },
        )
        self.assertEqual(
            Text('test', size=Text.LARGE).serialize(),
            {
                'object_type': 'text',
                'children': ['test'],
                'size': 'large',
            },
        )

    def test_button_component(self):
        self.assertEqual(
            Button([]).serialize(),
            {
                'object_type': 'button',
                'children': [],
                'action': [],
            },
        )

        class FakeAction:
            def serialize(self):
                return 'serialized_fake_action'

        self.assertEqual(
            Button([], action=FakeAction()).serialize(),
            {
                'object_type': 'button',
                'children': [],
                'action': ['serialized_fake_action'],
            },
        )

        self.assertEqual(
            Button([], action=[FakeAction(), FakeAction()]).serialize(),
            {
                'object_type': 'button',
                'children': [],
                'action': ['serialized_fake_action', 'serialized_fake_action'],
            },
        )

    def test_html_component(self):
        self.assertEqual(
            Html('test_content').serialize(),
            {
                'object_type': 'html',
                'children': [],
                'content': 'test_content',
            },
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
