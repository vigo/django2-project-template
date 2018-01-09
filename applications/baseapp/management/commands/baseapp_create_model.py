import os

from importlib import import_module

from django.conf import settings
from django.apps import apps
from django.core.management.base import (
    BaseCommand,
    CommandError,
)

from baseapp.management.template_structures import admins as admin_templates
from baseapp.management.template_structures import models as model_templates


TEMPLATE_MODELS = {
    'django': model_templates.TEMPLATE_MODEL_DJANGO,
    'basemodel': model_templates.TEMPLATE_MODEL_BASEMODEL,
    'softdelete': model_templates.TEMPLATE_MODEL_SOFTDELETEMODEL,
}

TEMPLATE_ADMINS = {
    'django': admin_templates.TEMPLATE_ADMIN_DJANGO,
    'basemodel': admin_templates.TEMPLATE_ADMIN_BASEMODEL,
    'softdelete': admin_templates.TEMPLATE_ADMIN_SOFTDELETEMODEL,
}

USER_REMINDER = """

    `{model_name}` related files created successfully:

    - `{app_name}/models/{model_name_lower}.py`
    - `{app_name}/admin/{model_name_lower}.py`

    Please check your models before running `makemigrations` ok?

"""


class Command(BaseCommand):
    help = (
        'Creates models/MODEL.py, admin/MODEL.py for given application'
    )

    MODEL_TYPE_CHOISES = [
        'django',
        'basemodel',
        'softdelete',
    ]

    def create_or_modify_file(self, filename, content, mode='w'):
        with open(filename, mode) as f:
            f.write(content)

    def add_arguments(self, parser):
        parser.add_argument('app_name', nargs=1, type=str, help='Name of your application')
        parser.add_argument('model_name', nargs=1, type=str, help='Name of your model')
        parser.add_argument(
            'model_type',
            nargs='?',
            default='django',
            choices=self.MODEL_TYPE_CHOISES,
            help='Type of your model')

    def handle(self, *args, **options):
        app_name = options.pop('app_name')[0]
        model_name = options.pop('model_name')[0]
        model_type = options.pop('model_type')

        try:
            import_module(app_name)
        except ImportError:
            raise CommandError(
                '%s is not exists. Please pass existing application name.' % app_name
            )

        if model_name.lower() in [model.__name__.lower() for model in apps.get_app_config(app_name).get_models()]:
            raise CommandError(
                '%s model is already exists in %s. Please try non-existing model name.' % (model_name, app_name)
            )

        app_dir = os.path.join(settings.BASE_DIR, 'applications', app_name)

        model_file = os.path.join(app_dir, 'models', '{}.py'.format(model_name.lower()))
        model_init_file = os.path.join(app_dir, 'models', '__init__.py')

        admin_file = os.path.join(app_dir, 'admin', '{}.py'.format(model_name.lower()))
        admin_init_file = os.path.join(app_dir, 'admin', '__init__.py')

        content_model_file = TEMPLATE_MODELS[model_type].format(
            model_name=model_name,
            app_name=app_name,
        )
        content_init_file = 'from .{} import *\n'.format(model_name.lower())

        content_admin_file = TEMPLATE_ADMINS[model_type].format(
            model_name=model_name,
            app_name=app_name,
        )

        self.create_or_modify_file(model_file, content_model_file)
        self.stdout.write(self.style.SUCCESS('models/{} created.'.format(os.path.basename(model_file))))

        self.create_or_modify_file(admin_file, content_admin_file)
        self.stdout.write(self.style.SUCCESS('admin/{} created.'.format(os.path.basename(admin_file))))

        self.create_or_modify_file(model_init_file, content_init_file, 'a')
        self.stdout.write(self.style.SUCCESS('{} model added to models/__init__.py'.format(model_name)))

        self.create_or_modify_file(admin_init_file, content_init_file, 'a')
        self.stdout.write(self.style.SUCCESS('{} model added to admin/__init__.py'.format(model_name)))

        self.stdout.write(self.style.NOTICE(USER_REMINDER.format(
            app_name=app_name,
            model_name=model_name,
            model_name_lower=model_name.lower(),
        )))
