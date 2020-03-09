from django.contrib.auth import get_user_model
from django_webtest import WebTest
from admin_list_controls.tests.test_app.wagtail_hooks import TestModelAdmin

User = get_user_model()


class TestAdmin(WebTest):
    def setUp(self):
        self.superuser = User.objects.create_superuser(
            username='test', email='test@example.com', password='test')

    def test_basic_rendering(self):
        test_model_list_view = TestModelAdmin().url_helper.index_url
        res = self.app.get(test_model_list_view, user=self.superuser)

        self.assertIn('__TEST_LAYOUT_TEMPLATE_CONTENT__', res.text)
        self.assertIn('admin_list_controls_initial_state', res.context)
        self.assertIn('admin_list_controls_selected_layout', res.context)
        self.assertIn('admin_list_controls_widget_js', res.context)
