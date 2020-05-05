from django.utils.translation import gettext as _
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from wagtail.contrib.modeladmin.views import IndexView
from admin_list_controls.views import ListControlsIndexViewMixin
from admin_list_controls.components import ListControls, Button, Icon, Text
from .models import Product


# TODO: allow modeladmin to control build+apply methods

class ProductAdminIndexView(IndexView, ListControlsIndexViewMixin):
    def build_list_controls(self):
        return ListControls([
            # Button(
            #     action=Something
            # )(
            #     Icon('icon-search'),
            #     Text('Some text component'),
            #     'An empty string',
            # ),
            # Button([
            #     Icon('icon-search'),
            #     Text('Some text component'),
            #     Text(size=Text.LARGE)(
            #         'Some text component'
            #     ),
            #     Panel(ref='some_id')(
            #         Text('something'),
            #         Button()('some text'),
            #     ),
            #     'An empty string',
            # ], action=Something),
            # Button()(
            #     Icon('icon-search'),
            #     Text('Some text component'),
            #     'An empty string',
            # ),
            # Button([
            #     Icon('icon-search'),
            #     Text('Some text component'),
            #     'An empty string',
            # ]),
            # Button()('An empty string'),
            # Button(['An empty string']),
        ])


@modeladmin_register
class ProductAdmin(ModelAdmin):
    model = Product
    index_view_class = ProductAdminIndexView
