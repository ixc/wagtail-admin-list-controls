from django.test import TestCase
from admin_list_controls.actions import BaseAction, SetValue, SubmitForm, TogglePanel, Link
from admin_list_controls.tests.utils import BaseTestCase


class TestActions(BaseTestCase):
    def test_base_action(self):
        self.assertEqual(
            BaseAction().serialize(),
            {
                'object_type': 'action',
                'action_type': '',
            },
        )

    def test_set_value_action(self):
        self.assertEqual(
            SetValue(name='test_name', value='test_value').serialize(),
            {
                'object_type': 'action',
                'action_type': 'set_value',
                'name': 'test_name',
                'value': 'test_value',
            },
        )
