from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from wagtail.contrib.modeladmin import views as modeladmin_views
from admin_list_controls.views import AdminListControlsMixin
from admin_list_controls.options import Filter, FilterGroup, FilterOptions, SortOptions, Sort, BOOLEAN_FILTER, \
    CHOICE_FILTER, STRING_FILTER, SORT_PARAM, LAYOUT_PARAM, Layout, LayoutOptions, ListViewOptions
from .models import TestModel


class TestModelAdminIndexView(AdminListControlsMixin, modeladmin_views.IndexView):
    def build_list_control_options(self):
        return ListViewOptions(
            filters=FilterOptions([
                Filter(
                    name='test_choice_filter',
                    label="Test choice filter",
                    results_description='test choice filter description',
                    type=CHOICE_FILTER,
                    choices=(
                        ('test one', 'Test one'),
                        ('test two', 'Test two'),
                    ),
                    multiple=True,
                    value='test one',
                ),
                Filter(
                    name='test_string_filter',
                    label="Test string filter",
                    results_description="test string filter description",
                    type=STRING_FILTER,
                    value='test',
                ),
                Filter(
                    name='test_boolean_filter',
                    label="Test boolean filter",
                    results_description="test boolean filter description",
                    type=BOOLEAN_FILTER,
                    value=True,
                ),
                FilterGroup(
                    title='Test filter group',
                    children=[
                        Filter(
                            name='test_nested_filter',
                            label="Test nested filter",
                            results_description="test nested filter description",
                            type=STRING_FILTER,
                            value='test',
                        ),
                    ]
                ),
            ]),
            sorts=SortOptions([
                Sort(
                    label='Test sort',
                    results_description='Test sort description',
                    value='test_sort',
                    is_selected=True,
                    is_default=True,
                ),
            ]),
            layouts=LayoutOptions([
                Layout(
                    label='Test layout with template',
                    value='test_layout_with_template',
                    is_selected=True,
                    icon_class='icon icon-fa-th',
                    template='test_app/test_layout.html'
                ),
                Layout(
                    label='Test layout without template',
                    value='test_layout_without_template',
                    is_selected=False,
                    icon_class='icon icon-fa-th-list',
                ),
            ]),
        )


@modeladmin_register
class TestModelAdmin(ModelAdmin):
    model = TestModel
    index_view_class = TestModelAdminIndexView
