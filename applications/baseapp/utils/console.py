import pprint
import shutil

DEBUG = True

try:
    from django.conf import settings
    DEBUG = settings.DEBUG
except BaseException:
    pass

TERMINAL_COLUMNS, TERMINAL_LINES = shutil.get_terminal_size()


__all__ = [
    'console',
]


class Console:
    """

    Usage:

        from baseapp.utils import console

    You can set default configuration such as:

        # main configuration example
        console.configure(
            char='x',
            source='console.py',
            width=8,             # demo purpose
            indent=8,            # demo purpose
            color='white',
        )

    Examples:

        console('Some', 'examples', 'of', 'console', 'usage')

        # change config on the fly
        console('Hello', 'World', 'Foo', 'Bar', 'Baz', width=12, indent=8, color='yellow')

        console.configure(color='default')
        console(['this', 'is', 'a', 'list'], ('and', 'a', 'tuple',))

    Available colors:

    - black
    - red
    - green
    - yellow
    - blue
    - magenta
    - cyan
    - white
    - default

    `console.dir()` inspired from Ruby's `inspection` style. This inspects
    most of the attributes of given Object.

    Examples:

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

        console.dir({})

    """

    __colors = dict(black=0, red=1, green=2, yellow=3, blue=4, magenta=5, cyan=6, white=7, default=8)
    __color = 'yellow'
    __color_reset = '\033[0m'

    __seperator_line = '{source:{char}<{length}}'
    __seperator_char = '*'

    def __init__(self, *args, **kwargs):
        self.__width = 79
        self.__indent = 4
        self.__source = __name__
        self.__call__(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        self.configure(**kwargs)
        self.print(*args, **kwargs)

    def dir(self, *args, **kwargs):
        for arg in args:
            out = {'arg': args}
            source_name = arg.__class__.__name__

            if source_name != 'type':
                source_name = 'instance of {}'.format(source_name)

            if hasattr(arg, '__name__'):
                source_name = arg.__name__

            source = '{} | {}'.format(source_name, type(arg))
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

                for obj_attr, obj_attr_val in arg.__dict__.items():
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

            self.print(out, source=source)

    def configure(self, **kwargs):
        self.width = kwargs.get('width', self.__width)
        self.indent = kwargs.get('indent', self.__indent)
        self.color = kwargs.get('color', self.__color)
        self.source = kwargs.get('source', self.__source)
        self.seperator_line = self.__seperator_line
        self.seperator_char = kwargs.get('char', self.__seperator_char)
        self.__width = self.width
        self.__indent = self.indent
        self.__color = self.color
        self.__source = self.source
        self.__seperator_char = self.seperator_char

    def colorize(self, color):
        if self.__colors.get(color, False):
            color_code = self.__colors.get(color)
        else:
            color_code = self.__colors.get(self.__color)
        return "\033[3{}m".format(color_code)

    def print(self, *args, **kwargs):
        if DEBUG:
            self.pp = pprint.PrettyPrinter(indent=self.indent, width=self.width, compact=True)
            if args:
                self.print_banner(**kwargs)
                self.pp.pprint(args)
                self.print_banner(source='', end='\n\n')

    def print_banner(self, **kwargs):
        pfmt = dict(
            source=kwargs.get('source', self.source + ' '),
            char=self.seperator_char,
            length=TERMINAL_COLUMNS,
        )
        end = '\n'
        if kwargs.get('end', False):
            end = kwargs.get('end')

        print(self.colorize(self.color) + self.seperator_line.format(**pfmt) + self.__color_reset, end=end)


if DEBUG:
    console = Console()
else:
    console = type('Console', (object,), dict())

    setattr(console, 'configure', lambda *args, **kwargs: '')
    setattr(console, 'dir', lambda *args, **kwargs: '')
    setattr(console, '__init__', lambda *args, **kwargs: None)
    setattr(console, '__call__', lambda *args, **kwargs: '')
