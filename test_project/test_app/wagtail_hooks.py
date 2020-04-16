from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from wagtail.contrib.modeladmin import views as modeladmin_views
from admin_list_controls.views import AdminListControlsMixin
from .models import TestModel


class TestModelAdminIndexView(AdminListControlsMixin, modeladmin_views.IndexView):
    pass


@modeladmin_register
class ImageAdmin(ModelAdmin):
    model = TestModel
    index_view_class = TestModelAdminIndexView

    search_fields = ('char_field',)
