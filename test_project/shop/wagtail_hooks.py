from django.utils.translation import gettext as _
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from wagtail.contrib.modeladmin.views import IndexView
from admin_list_controls.views import ListControlsIndexViewMixin
from admin_list_controls.components import ListControls, Button, Icon, Text, Panel, Divider, Block, Spacer
from admin_list_controls.actions import TogglePanel
from .models import Product


# TODO: allow modeladmin to control build+apply methods

class ProductAdminIndexView(ListControlsIndexViewMixin, IndexView):
    def build_list_controls(self):
        return ListControls()(
            Button(
                action=TogglePanel(ref='some_panel_ref'),
            )(
                Icon('icon icon-search'),
                Text('Some text component '),
                'A raw string',
            ),
            Button(
                action=TogglePanel(ref='some_other_panel_ref'),
            )('Second panel'),
            Panel(ref='some_panel_ref', collapsed=True)(
                Text('something'),
                Button()('some text'),
            ),
            Panel(ref='some_other_panel_ref')(
                Text('medium text ', size=Text.MEDIUM),
                Text('large text', size=Text.LARGE),
            ),
            Panel()(
                Text('medium text', size=Text.MEDIUM),
                Divider(),
                Text('Works large and bold text', size=Text.LARGE, style={'font-weight': 'bold'}),
                Spacer(),
                Text('medium text ', size=Text.MEDIUM),
                Text('medium and 200 weight text', size=Text.MEDIUM),
            ),
        )


@modeladmin_register
class ProductAdmin(ModelAdmin):
    model = Product
    index_view_class = ProductAdminIndexView
