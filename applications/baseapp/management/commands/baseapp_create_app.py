import os
import errno
import time

from importlib import import_module

from django.conf import settings
from django.core.management.base import (
    BaseCommand,
    CommandError,
)
from django.utils.text import capfirst


from baseapp.management.template_structures import application as application_templates


TEMPLATE_MODELS_INIT = """# from .MODEL_FILE import *

"""

TEMPLATE_ADMIN_INIT = """# from .ADMIN_FILE import *

"""

TEMPLATE_APP_INIT = """default_app_config = '{app_name}.apps.{app_name_capfirst}Config'
"""

APP_DIR_STRUCTURE = {
    'packages': [
        dict(name='admin', files=[
            dict(name='__init__.py', render=TEMPLATE_ADMIN_INIT),
        ]),
        dict(name='migrations'),
        dict(name='models', files=[
            dict(name='__init__.py', render=TEMPLATE_MODELS_INIT),
        ]),
    ],
    'templates': [
        dict(name='index.html', render=application_templates.TEMPLATE_HTML),
    ],
    'files': [
        dict(name='__init__.py', render=TEMPLATE_APP_INIT),
        dict(name='apps.py', render=application_templates.TEMPLATE_APPS),
        dict(name='urls.py', render=application_templates.TEMPLATE_URLS),
        dict(name='views.py', render=application_templates.TEMPLATE_VIEWS),
    ]
}

USER_REMINDER = """

    - Do not forget to add your `{app_name}` to `INSTALLED_APPS` under `config/settings/base.py`:

    INSTALLED_APPS += [
        '{app_name}',
    ]

    - Do not forget to fix your `config/settings/urls.py`:
    
    # ...
    urlpatterns = [
        # ...
        # this is just an example!
        path('__{app_name}__/', include('{app_name}.urls', namespace='{app_name}')),
        # ..
    ]
    # ...
"""


class Command(BaseCommand):
    help = (
        'Creates a custom Django app directory structure for the given app name in '
        '`applications/` directory.'
    )
    missing_args_message = 'You must provide an application name.'

    def add_arguments(self, parser):
        parser.add_argument('name', nargs=1, type=str, help='Name of your application')

    def handle(self, *args, **options):
        app_name = options.pop('name')[0]

        try:
            import_module(app_name)
        except ImportError:
            pass
        else:
            raise CommandError(
                '%r conflicts with the name of an existing Python module and '
                'cannot be used as an app name. Please try another name.' % app_name
            )

        applications_dir = os.path.join(settings.BASE_DIR, 'applications')
        templates_dir = os.path.join(settings.BASE_DIR, 'templates')
        new_application_dir = os.path.join(applications_dir, app_name)

        render_params = dict(
            app_name_title=app_name.title(),
            app_name=app_name,
            app_name_capfirst=capfirst(app_name),
        )

        self.mkdir(new_application_dir)
        self.touch(os.path.join(new_application_dir, '__init__.py'))

        for package in APP_DIR_STRUCTURE.get('packages'):
            package_dir = os.path.join(new_application_dir, package.get('name'))
            self.mkdir(package_dir)
            self.touch(os.path.join(package_dir, '__init__.py'))
            if package.get('files', False):
                self.generate_files(package.get('files'), package_dir, render_params)

        for template in APP_DIR_STRUCTURE.get('templates'):
            template_dir = os.path.join(templates_dir, app_name)
            template_html_path = os.path.join(template_dir, template.get('name'))
            self.mkdir(template_dir)
            self.touch(template_html_path)
            if template.get('render', False):
                rendered_content = template.get('render').format(**render_params)
                self.create_file_with_content(template_html_path, rendered_content)

        self.generate_files(APP_DIR_STRUCTURE.get('files'), new_application_dir, render_params)
        self.stdout.write(self.style.SUCCESS('"{}" application created.'.format(app_name)))
        self.stdout.write(self.style.NOTICE(USER_REMINDER.format(app_name=app_name)))

    def generate_files(self, files_list, root_path, render_params):
        for single_file in files_list:
            file_path = os.path.join(root_path, single_file.get('name'))
            self.touch(file_path)
            if single_file.get('render', False):
                rendered_content = single_file.get('render').format(**render_params)
                self.create_file_with_content(file_path, rendered_content)

    def mkdir(self, dirname):
        try:
            os.mkdir(dirname)
        except OSError as e:
            if e.errno == errno.EEXIST:
                message = '"%s" already exists' % dirname
            else:
                message = e
            raise CommandError(message)

    def create_file_with_content(self, filename, content):
        with open(filename, 'w') as f:
            f.write(content)

    def touch(self, filename):
        am_time = time.mktime(time.localtime())
        with open(filename, 'a'):
            os.utime(filename, (am_time, am_time))
