from django.test import TestCase
from admin_list_controls.components import ListControls, Block, Row, Column, Divider, Panel, \
    Icon, Text, Button, Html


class TestComponents(TestCase):
    def test_list_controls_component(self):
        self.assertEqual(
            ListControls().serialize(),
            {
                'object_type': 'list_controls',
                'children': None,
                'style': None,
            },
        )
        self.assertEqual(
            ListControls()(ListControls()).serialize(),
            {
                'object_type': 'list_controls',
                'children': [{
                    'object_type': 'list_controls',
                    'children': None,
                    'style': None,
                }],
                'style': None,
            },
        )

    def test_block_component(self):
        self.assertEqual(
            Block().serialize(),
            {
                'object_type': 'block',
                'children': None,
                'style': None,
            },
        )

    def test_row_component(self):
        self.assertEqual(
            Row().serialize(),
            {
                'object_type': 'row',
                'children': None,
                'style': None,
            },
        )

    def test_column_component(self):
        self.assertEqual(
            Column(width=Column.HALF_WIDTH).serialize(),
            {
                'object_type': 'column',
                'children': None,
                'width': 'half_width',
                'style': None,
            },
        )
        self.assertEqual(
            Column(width=Column.QUARTER_WIDTH).serialize(),
            {
                'object_type': 'column',
                'children': None,
                'width': 'quarter_width',
                'style': None,
            },
        )
        self.assertEqual(
            Column(width=Column.FULL_WIDTH).serialize(),
            {
                'object_type': 'column',
                'children': None,
                'width': 'full_width',
                'style': None,
            },
        )

    def test_divider_component(self):
        self.assertEqual(
            Divider().serialize(),
            {
                'object_type': 'divider',
                'children': None,
                'style': None,
            },
        )

    def test_panel_component(self):
        self.assertEqual(
            Panel().serialize(),
            {
                'object_type': 'panel',
                'children': None,
                'collapsed': False,
                'style': None,
            },
        )
        self.assertEqual(
            Panel(collapsed=True).serialize(),
            {
                'object_type': 'panel',
                'children': None,
                'collapsed': True,
                'style': None,
            },
        )
        self.assertEqual(
            Panel(collapsed=False).serialize(),
            {
                'object_type': 'panel',
                'children': None,
                'collapsed': False,
                'style': None,
            },
        )

    def test_icon_component(self):
        self.assertEqual(
            Icon(classes='test_class_name').serialize(),
            {
                'object_type': 'icon',
                'children': None,
                'classes': 'test_class_name',
                'style': None,
            },
        )

    def test_text_component(self):
        self.assertEqual(
            Text('').serialize(),
            {
                'object_type': 'text',
                'children': None,
                'content': '',
                'size': 'medium',
                'style': None,
            },
        )
        self.assertEqual(
            Text('test').serialize(),
            {
                'object_type': 'text',
                'children': None,
                'content': 'test',
                'size': 'medium',
                'style': None,
            },
        )
        self.assertEqual(
            Text('test', size=Text.MEDIUM).serialize(),
            {
                'object_type': 'text',
                'children': None,
                'content': 'test',
                'size': 'medium',
                'style': None,
            },
        )
        self.assertEqual(
            Text('test', size=Text.LARGE).serialize(),
            {
                'object_type': 'text',
                'children': None,
                'content': 'test',
                'size': 'large',
                'style': None,
            },
        )

    def test_button_component(self):
        self.assertEqual(
            Button().serialize(),
            {
                'object_type': 'button',
                'children': None,
                'action': [],
                'style': None,
            },
        )

        class FakeAction:
            def serialize(self):
                return 'serialized_fake_action'

        self.assertEqual(
            Button(action=FakeAction()).serialize(),
            {
                'object_type': 'button',
                'children': None,
                'action': ['serialized_fake_action'],
                'style': None,
            },
        )

        self.assertEqual(
            Button(action=[FakeAction(), FakeAction()]).serialize(),
            {
                'object_type': 'button',
                'children': None,
                'action': ['serialized_fake_action', 'serialized_fake_action'],
                'style': None,
            },
        )

    def test_html_component(self):
        self.assertEqual(
            Html('test_content').serialize(),
            {
                'object_type': 'html',
                'children': None,
                'content': 'test_content',
                'style': None,
            },
        )

    def test_nested_serialization(self):
        self.assertEqual(
            ListControls()(
                ListControls()(
                    ListControls(),
                ),
                ListControls()(
                    ListControls(),
                ),
            ).serialize(),
            {
                'object_type': 'list_controls',
                'children': [{
                    'object_type': 'list_controls',
                    'children': [{
                        'object_type': 'list_controls',
                        'children': None,
                        'style': None,
                    }],
                    'style': None,
                }, {
                    'object_type': 'list_controls',
                    'children': [{
                        'object_type': 'list_controls',
                        'children': None,
                        'style': None,
                    }],
                    'style': None,
                }],
                'style': None,
            }
        )

    def test_string_children_are_converted_to_text(self):
        self.assertEqual(
            ListControls()(
                'test string 1',
                'test string 2'
            ).serialize(),
            {
                'object_type': 'list_controls',
                'children': [
                    Text(content='test string 1').serialize(),
                    Text(content='test string 2').serialize(),
                ],
                'style': None,
            }
        )
