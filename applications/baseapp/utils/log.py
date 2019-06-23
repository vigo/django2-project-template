import json
import logging
import os
import urllib.request

from django.conf import settings
from django.utils import timezone
from django.utils.log import AdminEmailHandler

from ..utils import console

__all__ = ['SlackExceptionHandler']

logger = logging.getLogger('app')
console = console(source=__name__)


class SlackExceptionHandler(AdminEmailHandler):
    def emit(self, record):
        if os.environ.get('SLACK_HOOK', None):
            slack_message = [f'http status: {record.status_code}', f'timestamp: {timezone.now()}']
            try:
                request = record.request
                subject = '%s (%s IP): %s' % (
                    record.levelname,
                    ('internal' if request.META.get('REMOTE_ADDR') in settings.INTERNAL_IPS else 'EXTERNAL'),
                    record.getMessage(),
                )
                user_info = f'user_id: {request.user.id or "anonymous (None)"}'
                full_path = f'full path: {record.request.get_full_path()}'
            except Exception:  # pylint: disable=W0703
                subject = '%s: %s' % (record.levelname, record.getMessage())
                request = None
                user_info = None
                full_path = None

            exception_message = f'Exception: {",".join(record.exc_info[1].args)}'

            slack_message.append(subject)
            slack_message.append(exception_message)
            if user_info:
                slack_message.append(user_info)
            if full_path:
                slack_message.append(full_path)

            payload = dict(text='\n'.join(slack_message))
            response = urllib.request.urlopen(  # noqa: S310
                urllib.request.Request(
                    os.environ['SLACK_HOOK'],
                    data=json.dumps(payload).encode('utf8'),
                    headers={'content-type': 'application/json'},
                )
            )
            if response.read().decode('utf8') != 'ok':
                logger.error('Could not post to SLACK!')
