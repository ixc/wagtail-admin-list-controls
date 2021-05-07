from admin_list_controls.selectors import LayoutSelector
from admin_list_controls.views import ListControlsIndexView
from admin_list_controls.components import Button, Icon, Text, Panel, Divider, Block, Spacer, \
    Columns, Summary
from admin_list_controls.actions import TogglePanel, CollapsePanel, SubmitForm, Link
from admin_list_controls.filters import TextFilter, ChoiceFilter, RadioFilter, BooleanFilter, DateFilter
from wagtail.admin.staticfiles import versioned_static
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from .models import Product


class IndexView(ListControlsIndexView):
    def build_list_controls(self):
        return [
            Button(action=[
                TogglePanel(ref='panel_1'),
                CollapsePanel(ref='panel_2'),
            ])(
                Icon('icon icon-search'),
                'Filters',
            ),
            Button(action=[
                CollapsePanel(ref='panel_1'),
                TogglePanel(ref='panel_2'),
            ])(
                'Another panel'
            ),
            Button(action=Link('/some/url'))(
                Icon('icon icon-download'),
                'Export'
            ),
            Block(style={'float': 'right'})(
                LayoutSelector(value='grid')('Grid view'),
                LayoutSelector(value='list', is_default=True, style={'margin-left': '5px'})(
                    'List view'
                ),
            ),
            Panel(ref='panel_1', collapsed=True)(
                Text('Filters', size=Text.LARGE, style={'font-weight': 'bold'}),
                Spacer(),
                Columns()(
                    TextFilter(
                        name='text_filter',
                        label='A text filter',
                    ),
                    BooleanFilter(
                        name='bool_filter',
                        label='A boolean filter',
                    ),
                ),
                Divider(),
                Text('Another heading', size=Text.LARGE, style={'font-weight': 'bold'}),
                Spacer(),
                RadioFilter(
                    name='radio_filter',
                    label='A radio filter',
                    choices=(
                        ('', 'Any type'),
                        ('apple', 'Apple'),
                        ('banana', 'Banana'),
                        ('pear', 'Pear'),
                        ('persimmon', 'Persimmon'),
                        ('plum', 'Plum'),
                    ),
                    default_value='',
                ),
                Columns()(
                    ChoiceFilter(
                        name='choice_filter',
                        label='A choice filter',
                        choices=(
                            ('apple', 'Apple'),
                            ('banana', 'Banana'),
                            ('pear', 'Pear'),
                            ('persimmon', 'Persimmon'),
                            ('plum', 'Plum'),
                        ),
                    ),
                    ChoiceFilter(
                        name='multiple_choice_filter',
                        label='A multiple choice filter',
                        choices=(
                            ('apple', 'Apple'),
                            ('banana', 'Banana'),
                            ('pear', 'Pear'),
                            ('persimmon', 'Persimmon'),
                            ('plum', 'Plum'),
                        ),
                        multiple=True,
                    ),
                ),
                Spacer(),
                Button(action=SubmitForm())('Apply filters'),
            ),
            Panel(ref='panel_2', collapsed=True)(
                Text('medium text ', size=Text.MEDIUM),
                Text('large text', size=Text.LARGE),
                DateFilter(
                    name='date_start',
                    label='Date',
                    format='%d/%m/%Y',
                ),
                Spacer(),
                Button(action=SubmitForm())('Apply filters'),
            ),
            Summary(),
        ]


@modeladmin_register
class ProductAdmin(ModelAdmin):
    model = Product
    index_view_class = IndexView
    search_fields = ('name',)

    index_view_extra_js = [versioned_static(
        'wagtailadmin/js/date-time-chooser.js')]
