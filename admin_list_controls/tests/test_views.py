from django.contrib.auth import get_user_model
from django.test import RequestFactory
from wagtail.contrib.modeladmin.options import ModelAdmin
from django_webtest import WebTest
from shop.models import Product
from admin_list_controls.views import ListControlsIndexView


User = get_user_model()


class TestViews(WebTest):
    def setUp(self):
        self.factory = RequestFactory()
        self.superuser = User.objects.create_superuser(
            username='test',
            email='test@example.com',
            password='test',
        )

    def tearDown(self):
        User.objects.all().delete()

    def test_view_init_and_context(self):
        class TestView(ListControlsIndexView):
            pass

        view = self.list_view_class_to_view_function(TestView)
        response = view(self.create_superuser_request('/'))
        self.assertIn('admin_list_controls', response.context_data)
        self.assertIsInstance(response.context_data['admin_list_controls'], dict)

    def create_superuser_request(self, url):
        request = self.factory.get(url)
        request.user = self.superuser
        return request

    def instantiate_list_view_class(self, list_view_class) -> ListControlsIndexView:
        class TestModelAdmin(ModelAdmin):
            model = Product
            index_view_class = list_view_class

        return list_view_class(model_admin=TestModelAdmin())

    def list_view_class_to_view_function(self, list_view_class):
        class TestModelAdmin(ModelAdmin):
            model = Product
            index_view_class = list_view_class

        request = self.factory.get('/')
        request.user = self.superuser
        return TestModelAdmin().index_view
