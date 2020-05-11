from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from wagtail.contrib.modeladmin.views import IndexView

from admin_list_controls.selectors import Layout
from admin_list_controls.views import ListControlsIndexViewMixin
from admin_list_controls.components import ListControls, Button, Icon, Text, Panel, Divider, Block, Spacer
from admin_list_controls.actions import TogglePanel, ClosePanel, SubmitForm
from admin_list_controls.filters import TextFilter, ChoiceFilter, RadioFilter, BooleanFilter
from .models import Product


# TODO: allow modeladmin to control build+apply methods

class ProductAdminIndexView(ListControlsIndexViewMixin, IndexView):
    def build_list_controls(self):
        return ListControls()(
            Button(action=[
                TogglePanel(ref='panel_1'),
                ClosePanel(ref='panel_2'),
            ])(
                Icon('icon icon-search'),
                'Filters',
            ),
            Button(action=[
                ClosePanel(ref='panel_1'),
                TogglePanel(ref='panel_2'),
            ])(
                'Another panel'
            ),
            Block(style={'float': 'right'})(
                Layout(value='grid')('Grid view'),
                Layout(value='list', is_default=True, style={'margin-left': '5px'})(
                    'List view'
                ),
            ),
            Panel(ref='panel_1')(
                Text('Filters', size=Text.LARGE, style={'font-weight': 'bold'}),
                Spacer(),
                TextFilter(
                    name='text_filter',
                    label='A text filter',
                ),
                BooleanFilter(
                    name='bool_filter',
                    label='A boolean filter',
                ),
                Divider(),
                Text('Another heading', size=Text.LARGE, style={'font-weight': 'bold'}),
                Spacer(),
                RadioFilter(
                    name='radio_filter',
                    label='A radio filter',
                    choices=(
                        ('', 'Empty choice'),
                        ('apple', 'Apple'),
                        ('banana', 'Banana'),
                        ('pear', 'Pear'),
                        ('persimmon', 'Persimmon'),
                        ('plum', 'Plum'),
                    ),
                    default_value='',
                ),
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
                Spacer(),
                Button(action=SubmitForm())('Apply filters'),
            ),
            Panel(ref='panel_2', collapsed=True)(
                Text('medium text ', size=Text.MEDIUM),
                Text('large text', size=Text.LARGE),
            ),
        )


@modeladmin_register
class ProductAdmin(ModelAdmin):
    model = Product
    index_view_class = ProductAdminIndexView
