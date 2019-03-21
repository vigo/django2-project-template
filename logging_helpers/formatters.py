import logging
import re

from django.core.management.color import color_style

__all__ = ['CustomWerkzeugLogFormatter', 'CustomSqlLogFormatter']

ansi_escape = re.compile(r'\x1b[^m]*m')


class CustomWerkzeugLogFormatter(logging.Formatter):
    def __init__(self, *args, **kwargs):
        self.style = color_style()
        super().__init__(*args, **kwargs)

    def status_code(self, message):
        match = re.search(r' (\d+) -$', message)
        if match:
            return int(match.groups()[0])
        else:
            return None

    def format(self, record):  # noqa: A003
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
        record.levelname = '{0:.<14}'.format(record.levelname)

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

    def format(self, record):  # noqa: A003
        record.levelname = '{0:.<14}'.format('SQL')
        record.levelname = self.style.HTTP_INFO(record.levelname)
        record.sql = self.style.SQL_KEYWORD(record.sql)
        return super().format(record)
