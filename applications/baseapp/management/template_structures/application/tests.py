TEMPLATE_TESTS = """from django.test import TestCase

from baseapp.utils import console

__all__ = [
    '{app_name_title}BasicTestCase',
]

console = console(source=__name__)


class {app_name_title}BasicTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):  # noqa: N802
        cls.hello = 'world'

    def test_hello_world(self):
        self.assertEqual(self.hello, 'world')

"""


__all__ = [
    'TEMPLATE_TESTS',
]
