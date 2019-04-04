# pylint: disable=W0223

from django.core.management.base import BaseCommand


class CustomBaseCommand(BaseCommand):
    """

    CustomBaseCommand comes with a small method. `.out()` is a helper.

    Usage:

        class Command(CustomBaseCommand):
            def handle(self, *args, **options):
                self.out('hello')       # INFO
                self.out('hello', 'w')  # WARNING
                self.out('hello', 'e')  # ERROR
                self.out('hello', 'n')  # NOTICE

    """

    def out(self, text, style='s'):
        switcher = {'s': 'SUCCESS', 'w': 'WARNING', 'e': 'ERROR', 'n': 'NOTICE'}.get(style, 's')
        writer = getattr(self.style, switcher)
        self.stdout.write(writer(text))
