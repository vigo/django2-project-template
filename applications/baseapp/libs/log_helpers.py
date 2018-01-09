import re
import logging

from django.conf import settings
from django.core.management.color import color_style

ansi_escape = re.compile(r'\x1b[^m]*m')


class CustomWerkzeugLogFormatter(logging.Formatter):
    def __init__(self, *args, **kwargs):
        self.style = color_style()
        super().__init__(*args, **kwargs)

    def status_code(self, message):
        match = re.search(' (\d+) -$', message)
        if match:
            return int(match.groups()[0])
        else:
            return None

    def format(self, record):
        msg = ansi_escape.sub('', record.msg)
        status_code = self.status_code(msg)

        if status_code:
            if 200 <= status_code < 300:
                msg = self.style.HTTP_SUCCESS(msg)
            elif 100 <= status_code < 200:
                msg = self.style.HTTP_INFO(msg)
            elif status_code == 304:
                msg = self.style.HTTP_NOT_MODIFIED(msg)
            elif 300 <= status_code < 400:
                msg = self.style.HTTP_REDIRECT(msg)
            elif status_code == 404:
                msg = self.style.HTTP_NOT_FOUND(msg)
            elif 400 <= status_code < 500:
                msg = self.style.HTTP_BAD_REQUEST(msg)
            else:
                msg = self.style.HTTP_SERVER_ERROR(msg)

        levelname = record.levelname.lower()
        levelstyle = self.style.SUCCESS
        record.levelname = '{:.<14}'.format(record.levelname)

        if levelname == 'warning':
            levelstyle = self.style.WARNING
        elif levelname == 'info':
            levelstyle = self.style.HTTP_INFO
        elif levelname == 'error':
            levelstyle = self.style.ERROR
        else:
            levelstyle = self.style.NOTICE

        record.levelname = levelstyle(record.levelname)
        record.msg = msg
        return super().format(record)


class CustomSqlLogFormatter(logging.Formatter):
    def __init__(self, *args, **kwargs):
        self.style = color_style()
        super().__init__(*args, **kwargs)

    def format(self, record):
        record.levelname = '{:.<14}'.format('SQL')
        record.levelname = self.style.HTTP_INFO(record.levelname)
        record.sql = self.style.SQL_KEYWORD(record.sql)
        return super().format(record)


def werkzueg_filter_extenstions_callback(record):
    if getattr(settings, 'CUSTOM_LOGGER_OPTIONS', False):
        hide_these_extensions = settings.CUSTOM_LOGGER_OPTIONS.get('hide_these_extensions', False)
        if hide_these_extensions:
            return not any(['.{}'.format(ext) in record.msg for ext in hide_these_extensions])
    else:
        return True
