from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from wagtail.contrib.modeladmin import views as modeladmin_views
from admin_list_controls.views import AdminListControlsMixin
from admin_list_controls.options import StringFilter, RadioFilter, ChoiceFilter, BooleanFilter, FilterGroup, \
    FilterPanel, SortPanel, Sort, Layout, LayoutOptions, ListViewControls
from .models import TestModel


class TestModelAdminIndexView(AdminListControlsMixin, modeladmin_views.IndexView):
    def build_list_controls(self):
        return ListViewControls([
            FilterPanel([
                ChoiceFilter(
                    name='test_choice_filter',
                    label="Test choice filter",
                    results_description='test choice filter description',
                    choices=(
                        ('test one', 'Test one'),
                        ('test two', 'Test two'),
                    ),
                    multiple=True,
                    value='test one',
                ),
                StringFilter(
                    name='test_string_filter',
                    label="Test string filter",
                    results_description="test string filter description",
                    value='test',
                ),
                BooleanFilter(
                    name='test_boolean_filter',
                    label="Test boolean filter",
                    results_description="test boolean filter description",
                    value=True,
                ),
                RadioFilter(
                    name='test_radio_filter',
                    label="Test radio filter",
                    results_description="test radio filter description",
                    choices=(
                        ('test one', 'Test one'),
                        ('test two', 'Test two'),
                    ),
                    value='test one',
                ),
                FilterGroup(
                    title='Test filter group',
                    children=[
                        StringFilter(
                            name='test_nested_filter',
                            label="Test nested filter",
                            results_description="test nested filter description",
                            value='test',
                        ),
                    ]
                ),
            ]),
            SortPanel([
                Sort(
                    label='Test sort',
                    results_description='Test sort description',
                    value='test_sort',
                    is_selected=True,
                    is_default=True,
                ),
            ]),
            LayoutOptions([
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
            ])
        ])


@modeladmin_register
class TestModelAdmin(ModelAdmin):
    model = TestModel
    index_view_class = TestModelAdminIndexView
