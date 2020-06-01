# wagtail-admin-list-controls

A UI toolkit that extends Wagtail's admin list views and allows you to build custom filters, buttons, panels and more.

![](./docs/screenshots/image_list_view_default.png)


- [Installation](#installation)
- [Documentation](#documentation)
- [Rationale and goals](#rationale-and-goals)
- [Project setup](#project-setup)
- [Test suite](#test-suite)
- [Building the project](#building-the-project)


## Installation

```
pip install wagtail-admin-list-controls
```

and add `'admin-list-controls'` to `INSTALLED_APPS` in your settings.


## Documentation

### Basic usage

The following example provides a text input that allows the user to perform textual queries against
a related model's `name` field.. 

```python
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from admin_list_controls.views import ListControlsIndexView
from admin_list_controls.components import Button, Panel
from admin_list_controls.actions import SubmitForm
from admin_list_controls.filters import TextFilter


class IndexView(ListControlsIndexView):
        def build_list_controls(self):
            return [
                Panel()(
                    TextFilter(
                        name="text_filter",
                        label="Creator's name",
                        apply_to_queryset=lambda queryset, value: queryset.filter(created_by__name__icontains=value)
                    ),
                    Button(action=SubmitForm())(
                        "Apply filters",
                    ),
                ),
            ]


@modeladmin_register
class MyModelAdmin(ModelAdmin):
    index_view_class = IndexView
    # ...
```

The code above should give you a UI that looks like

![](./docs/screenshots/basic_usage_example.png)


## Rationale and goals

This library emerged from a large build that required an admin list view with an exhaustive set of filters and the 
ability for users to change the ordering of the results. The filters would need to perform exact and substring matching 
against textual fields, as well as exact matches on boolean and choice fields. Some of the sorts applied to order the 
results also relied on complicated querying and conditional behaviours. In some extreme conditions, certain 
combinations of filters and sorts would require distinct code paths.

We initially attempted to use Wagtail's built-in searching and filtering features, but they were found to be too 
limiting for our use-cases and resulted in a non-optimal experience for users. Third-party libraries were 
investigated, but the ecosystem doesn't have much covering the space.

Somewhat reluctantly, this library was built to cover our needs. Now that the dust has settled and the code has 
stabilised, we're finding increasing numbers of use-cases for it.


## Project setup

```
# Frontend
npm install
npm run build
```

```
# Backend
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
./test_project/manage.py migrate
```


## Test suite

```
./test_project/manage.py test admin_list_controls
```


## Building the project

### Building the frontend

```
# Development (file watchers, no optimisation, etc)
npm run build-dev

# Production/release
npm run build
```

### Building the project for release

```
npm run build
rm -rf dist/
python setup.py sdist bdist_wheel
python setup.py upload
```
