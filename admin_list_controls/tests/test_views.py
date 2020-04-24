from django.contrib.auth import get_user_model
from django.test import RequestFactory
from wagtail.contrib.modeladmin.options import ModelAdmin
from django_webtest import WebTest
from shop.models import Product
from admin_list_controls.views import ListControlsIndexView
from admin_list_controls.base_controls import BaseFilter, BaseToggle
from admin_list_controls.controls import TextFilter, BooleanFilter, ChoiceFilter, \
    MultipleChoiceFilter, RadioFilter, Sort, Layout, ListControls, FilterPanel, \
    FilterGroup, SortPanel, LayoutControls


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

    def test_view_can_aggregate_filters(self):
        class TestView(ListControlsIndexView):
            def build_list_controls(self):
                return ListControls([
                    TextFilter(name='test_name_1'),
                    TextFilter(name='test_name_2'),
                    FilterPanel([
                        TextFilter(name='test_name_3'),
                        FilterPanel([
                            TextFilter(name='test_name_4'),
                        ]),
                    ]),
                    FilterPanel([
                        TextFilter(name='test_name_5'),
                    ]),
                    TextFilter(name='test_name_6'),
                ])

        view_class = self.instantiate_list_view_class(TestView)
        filters = view_class.get_list_control_filters()
        filter_names = [obj.name for obj in filters]
        self.assertEqual(filter_names, [
            'test_name_1',
            'test_name_2',
            'test_name_3',
            'test_name_4',
            'test_name_5',
            'test_name_6',
        ])

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
