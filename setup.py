import setuptools
import admin_list_controls

setuptools.setup(
    name='wagtail-admin-list-controls',
    version=admin_list_controls.__version__,
    author='Interaction Consortium',
    author_email='studio@interaction.net.au',
    url='https://github.com/ixc/wagtail-admin-list-controls',
    description='A UI toolkit to build custom filtering and other functionalities into wagtail\'s admin list views.',
    long_description='Documentation at https://github.com/ixc/wagtail-admin-list-controls',
    license='MIT',
    packages=setuptools.find_packages(),
    include_package_data=True,
)
