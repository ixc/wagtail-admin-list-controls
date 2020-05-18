# wagtail-admin-list-controls

A UI toolkit to build custom filtering and other functionalities into your admin list views.

![Collapsible "Advanced Search" and "Order Results" panels with buttons to change layouts](./docs/screenshots/image_list_view_default.png)

Note that the project is currently in early release and is currently undergoing significant API churn.
Documenation should be forthcoming once everything settles. If you'd like to use the system, the closest
thing to docs will be the test cases and test project.


- [Installation](#installation)
- [Documentation](#documentation)
- [Rationale and goals](#rationale-and-goals)
- [Test suite](#test-suite)
- [Building the project](#building-the-project)


## Installation

```
pip install wagtail-admin-list-controls
```


## Documentation


**TODO** see test suite + test project for code examples.


## Rationale and goals

This library emerged from a large build that required an admin list view with an exhaustive set of filters and the 
ability for users to change the ordering of the results. The filters would need to perform exact and substring matching 
against textual fields, as well as exact matches on boolean and choice fields. Some of the sorts applied to order the 
results also relied on complicated querying and conditional behaviour (eg: certain filter+sort combinations required 
different code paths).

We initially attempted to use Wagtail's built-in searching and filtering features, but they were found to a be too 
limiting for our use-cases and resulted in a non-optimal experience for users. Third-party libraries were 
investigated, but there wasn't much in the ecosystem

Somewhat reluctantly, this library was built to cover our needs. Now that the dust has settled and the code has 
stabilised, we're finding increasing numbers of use-cases for it.


## Test suite

```
# Setup
npm install
npm run build
pip install -r requirements.txt
./manage.py migrate
```

```
# Run the tests
./manage.py test admin_list_controls
```


## Building the project

### Build for development

```
# Frontend
npm install
npm run build-dev
```

```
# Backend
pip install -r requirements.txt
./manage.py migrate
./manage.py runserver
```


### Build for release

```
npm install
npm run build
rm -rf dist/
python setup.py sdist bdist_wheel
python setup.py upload
``` 
