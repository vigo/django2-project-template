from django.core.exceptions import PermissionDenied
from django.shortcuts import render

from ..utils import console

__all__ = ['custom_400_error', 'custom_403_error', 'custom_404_error', 'custom_500_error']

console = console(source=__name__)


def exception_message(exception):
    exception_repr = exception.__class__.__name__
    if not exception:
        return None
    try:
        message = exception.args[0]
    except (AttributeError, IndexError):
        pass
    else:
        if isinstance(message, str):
            exception_repr = message
    return exception_repr


def custom_400_error(request, exception=None, template_name='custom_errors/400.html'):
    context = {'request_path': request.path, 'exception': exception_message(exception)}
    return render(request, template_name=template_name, context=context, status=400)


def custom_403_error(request, exception=None, template_name='custom_errors/403.html'):
    if exception is None:
        raise PermissionDenied
    context = {'request_path': request.path, 'exception': exception_message(exception)}
    return render(request, template_name=template_name, context=context, status=403)


def custom_404_error(request, exception=None, template_name='custom_errors/404.html'):
    context = {'request_path': request.path, 'exception': exception_message(exception)}
    return render(request, template_name=template_name, context=context, status=404)


def custom_500_error(request, template_name='custom_errors/500.html'):
    context = {'request_path': request.path}
    return render(request, template_name=template_name, context=context, status=500)
