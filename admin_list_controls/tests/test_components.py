from admin_list_controls.components import ListControls, Block, Spacer, Columns, Divider, Panel, \
    Icon, Text, Button, Summary
from admin_list_controls.tests.utils import BaseTestCase


class TestComponents(BaseTestCase):
    def test_list_controls_component(self):
        self.assertObjectSerializesTo(
            ListControls(),
            {
                'object_type': 'list_controls',
                'children': None,
                'style': None,
            },
        )
        serialized = ListControls().serialize()
        self.assertEqual(serialized['extra_classes'], None)
        self.assertIn('ListControls', serialized['component_id'])
        nested = ListControls()
        self.assertObjectSerializesTo(
            ListControls()(nested),
            {
                'object_type': 'list_controls',
                'children': [nested.serialize()],
            },
        )

    def test_block_component(self):
        self.assertObjectSerializesTo(
            Block(),
            {
                'object_type': 'block',
            },
        )

    def test_spacer_component(self):
        self.assertObjectSerializesTo(
            Spacer(),
            {
                'object_type': 'block',
                'style': {'paddingTop': '20px'},
            },
        )

    def test_columns_component(self):
        component = Columns()(
            [Text('Column 1')],
            ['Column 2'],
        )
        component.prepare_children()
        serialized = component.serialize()
        self.assertEqual(serialized['object_type'], 'columns')
        self.assertEqual(len(serialized['children']), 2)
        self.assertDictContainsSubset(
            {
                'object_type': 'block',
                'style': {
                    'width': 'calc((100% - ((2 - 1) * 10px)) / 2)',
                    'float': 'left',
                    'marginLeft': '0',
                },
            },
            serialized['children'][0],
        )
        self.assertDictContainsSubset(
            {
                'object_type': 'text',
                'content': 'Column 1',
            },
            serialized['children'][0]['children'][0],
        )
        self.assertDictContainsSubset(
            {
                'object_type': 'block',
                'style': {
                    'width': 'calc((100% - ((2 - 1) * 10px)) / 2)',
                    'float': 'left',
                    'marginLeft': '10px',
                },
            },
            serialized['children'][1],
        )
        self.assertDictContainsSubset(
            {
                'object_type': 'text',
                'content': 'Column 2',
            },
            serialized['children'][1]['children'][0],
        )

    def test_divider_component(self):
        self.assertObjectSerializesTo(
            Divider(),
            {
                'object_type': 'divider',
            },
        )

    def test_panel_component(self):
        self.assertObjectSerializesTo(
            Panel(),
            {
                'object_type': 'panel',
                'collapsed': False,
            },
        )
        self.assertObjectSerializesTo(
            Panel(collapsed=True),
            {
                'object_type': 'panel',
                'collapsed': True,
            },
        )
        self.assertObjectSerializesTo(
            Panel(collapsed=False),
            {
                'object_type': 'panel',
                'collapsed': False,
            },
        )

    def test_icon_component(self):
        self.assertObjectSerializesTo(
            Icon(classes='test_class_name'),
            {
                'object_type': 'icon',
                'extra_classes': 'test_class_name',
            },
        )

    def test_text_component(self):
        self.assertObjectSerializesTo(
            Text(''),
            {
                'object_type': 'text',
                'content': '',
                'size': 'medium',
            },
        )
        self.assertObjectSerializesTo(
            Text('test'),
            {
                'object_type': 'text',
                'content': 'test',
                'size': 'medium',
            },
        )
        self.assertObjectSerializesTo(
            Text('test', size=Text.MEDIUM),
            {
                'object_type': 'text',
                'content': 'test',
                'size': 'medium',
            },
        )
        self.assertObjectSerializesTo(
            Text('test', size=Text.LARGE),
            {
                'object_type': 'text',
                'content': 'test',
                'size': 'large',
            },
        )

    def test_button_component(self):
        self.assertObjectSerializesTo(
            Button(),
            {
                'object_type': 'button',
                'action': [],
            },
        )

        class FakeAction:
            def serialize(self):
                return 'serialized_fake_action'

        self.assertObjectSerializesTo(
            Button(action=FakeAction()),
            {
                'object_type': 'button',
                'action': ['serialized_fake_action'],
            },
        )

        self.assertObjectSerializesTo(
            Button(action=[FakeAction(), FakeAction()]),
            {
                'object_type': 'button',
                'action': ['serialized_fake_action', 'serialized_fake_action'],
            },
        )

    def test_summary_component(self):
        self.assertObjectSerializesTo(
            Summary(),
            {
                'object_type': 'summary',
                'summary': [],
                'reset_label': 'Reset all',
            },
        )

    def test_string_children_are_converted_to_text_components(self):
        serialized = ListControls()(
            'test string 1',
            'test string 2'
        ).serialize()
        self.assertDictContainsSubset(
            {
                'object_type': 'text',
                'content': 'test string 1',
            },
            serialized['children'][0],
        )
        self.assertDictContainsSubset(
            {
                'object_type': 'text',
                'content': 'test string 2',
            },
            serialized['children'][1],
        )
