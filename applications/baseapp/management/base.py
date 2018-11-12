from django.core.management.base import BaseCommand


class CustomBaseCommand(BaseCommand):
    def out(self, text, style='s'):
        switcher = {
            's': 'SUCCESS',
            'w': 'WARNING',
            'e': 'ERROR',
            'n': 'NOTICE',
        }.get(style, 's')
        writer = getattr(self.style, switcher)
        self.stdout.write(writer(text))
