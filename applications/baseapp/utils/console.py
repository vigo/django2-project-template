# pylint: disable=R0912,W0603

import os
import pprint
import shutil
import sys

DEBUG = False

try:
    from django.conf import settings

    DEBUG = settings.DEBUG
except BaseException:
    pass

TERMINAL_COLUMNS, TERMINAL_LINES = shutil.get_terminal_size()


__all__ = ['console']


class Console:
    """

    Custom object inspector. Example usage:

        from ..utils import console         # or
        from baseapp.utils import console

        console = console(
            source=__name__,
        )

        # or
        console = console(
            source=__name__,
            indent=8,
            width=64,
        )

        # or
        console = console(
            source=__name__,
            color='yellow',
        )

        # after setting console, now try:

        console('hello', 'world', [1, 2, 3])
        console('hello', 'world', [1, 2, 3], color='red')

        # for more complex objects;

        class MyClass:
            klass_var1 = 1
            klass_var2 = 2

            def __init__(self):
                self.name = 'Name'

            def start(self):
                return 'method'

            @property
            def admin(self):
                return True

            @staticmethod
            def statik():
                return 'Static'

            @classmethod
            def klass_method(cls):
                return 'kls'

        mc = MyClass()

        console.dir(MyClass)
        console.dir(mc)
        console.dir(dict)

    """

    valid_options = ['source', 'width', 'indent', 'color']
    available_colors = dict(black=0, red=1, green=2, yellow=3, blue=4, magenta=5, cyan=6, white=7, default=8)

    defaults_options = {
        'source': 'UNSET',
        'width': 79,
        'indent': 4,
        'seperator_line': '{source:{char}<{width}}',
        'seperator_char': '*',
        'color': 'yellow',
    }

    def __init__(self, **options):
        self.options = {}
        self.pp = None

        for (default_option, default_value) in self.defaults_options.items():
            self.options[default_option] = default_value
        self.configure(**options)

    def configure(self, **options):
        for option, value in options.items():
            if option in self.valid_options:
                self.options[option] = value
            else:
                raise Exception(f'Invalid option: [{option}] passed')

        color = self.options['color']
        if color not in self.available_colors.keys():
            raise Exception(f'Invalid color value: [{color}] passed')

        if not isinstance(self.options['width'], int):
            raise Exception('Invalid width value. Expected int, got: [{0}]'.format(type(self.options['width'])))

        if not isinstance(self.options['indent'], int):
            raise Exception('Invalid indent value. Expected int, got: [{0}]'.format(type(self.options['indent'])))

    def colorize(self, input_string):
        return '\033[3{0}m{1}{2}'.format(self.available_colors[self.options['color']], input_string, '\033[0m')

    def __call__(self, *args, **options):
        if args:
            self.oprint(args, **options)

    def dir(self, *args, **options):  # noqa: A003
        out = {}
        for arg in args:
            source_name = arg.__class__.__name__

            if source_name != 'type':
                source_name = 'instance of {0}'.format(source_name)

            if hasattr(arg, '__name__'):
                source_name = arg.__name__

            source = '{0} | {1}'.format(source_name, type(arg))

            public_attributes = []
            internal_methods = []
            private_methods = []

            for object_method in dir(arg):
                if object_method.startswith('__'):
                    internal_methods.append(object_method)
                elif object_method.startswith('_'):
                    private_methods.append(object_method)
                else:
                    public_attributes.append(object_method)

            if public_attributes:
                out.update(public_attributes=public_attributes)
            if internal_methods:
                out.update(internal_methods=internal_methods)
            if private_methods:
                out.update(private_methods=private_methods)

            if hasattr(arg, '__dict__'):
                property_list = []
                static_methods = []
                class_methods = []
                public_methods = []

                for (obj_attr, obj_attr_val) in arg.__dict__.items():
                    _name = type(obj_attr_val).__name__

                    if _name == 'property':
                        property_list.append(obj_attr)
                        if obj_attr in public_attributes:
                            public_attributes.remove(obj_attr)

                    if _name == 'staticmethod':
                        static_methods.append(obj_attr)
                        if obj_attr in public_attributes:
                            public_attributes.remove(obj_attr)

                    if _name == 'classmethod':
                        class_methods.append(obj_attr)
                        if obj_attr in public_attributes:
                            public_attributes.remove(obj_attr)

                    if _name == 'function':
                        public_methods.append(obj_attr)
                        if obj_attr in internal_methods:
                            internal_methods.remove(obj_attr)
                        if obj_attr in public_attributes:
                            public_attributes.remove(obj_attr)

                if property_list:
                    out.update(property_list=property_list)
                if static_methods:
                    out.update(static_methods=static_methods)
                if class_methods:
                    out.update(class_methods=class_methods)
                if public_methods:
                    out.update(public_methods=public_methods)

                if not arg.__dict__.get('__init__', False):
                    instance_attributes = []
                    for instance_attr in list(arg.__dict__.keys()):
                        instance_attributes.append(instance_attr)
                        if instance_attr in public_attributes:
                            public_attributes.remove(instance_attr)
                        if instance_attr in public_methods:
                            public_methods.remove(instance_attr)
                    out.update(instance_attributes=instance_attributes)

            options.update(source=source)
            self.oprint(out, **options)

    def oprint(self, input_txt, **options):
        source = self.options['source']

        if 'source' in options.keys():
            source = '{0} : {1}'.format(source, options.pop('source'))

        self.configure(**options)

        self.pp = pprint.PrettyPrinter(indent=self.options['indent'], width=self.options['width'], compact=True)

        header = self.options['seperator_line'].format(
            source='[{0}]'.format(source), char=self.options['seperator_char'], width=self.options['width']
        )
        footer = self.options['seperator_char'] * self.options['width']

        sys.stdout.write(self.colorize(header))
        sys.stdout.write('\n')
        self.pp.pprint(input_txt)
        sys.stdout.write(self.colorize(footer))
        sys.stdout.write('\n' * 2)


def console(**options):
    global DEBUG, TERMINAL_COLUMNS

    if DEBUG or os.getenv('DJANGO_ENV', 'not_available') == 'test':
        if 'width' not in options.keys():
            options.update(width=TERMINAL_COLUMNS)
        return Console(**options)

    c = type('Console', (object,), dict())
    setattr(c, 'dir', lambda *args, **kwargs: '')  # noqa: B010
    setattr(c, '__init__', lambda *args, **kwargs: None)  # noqa: B010
    setattr(c, '__call__', lambda *args, **kwargs: '')  # noqa: B010
    return c
