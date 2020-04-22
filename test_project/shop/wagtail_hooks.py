from django.utils.translation import gettext as _
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from wagtail.contrib.modeladmin.views import IndexView
from admin_list_controls.views import ListControlsIndexViewMixin
from admin_list_controls.controls import ListControls, MultipleChoiceFilter, FilterPanel
from .models import Product


# TODO: allow modeladmin to control build+apply methods

class ProductAdminIndexView(IndexView, ListControlsIndexViewMixin):
    def build_list_controls(self):
        return ListControls([
            FilterPanel(
                label=_('Advanced search'),
                children=[
                    MultipleChoiceFilter(
                        name='product_type',
                        label=_('Colour'),
                        choices=Product.PRODUCT_TYPE_CHOICES,
                        apply_to_queryset=lambda queryset, values: queryset.filter(product_type__in=values),
                    ),
                ],
            ),
        ])


@modeladmin_register
class ProductAdmin(ModelAdmin):
    model = Product
    index_view_class = ProductAdminIndexView
