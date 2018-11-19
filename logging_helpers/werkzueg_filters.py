from django.conf import settings

__all__ = ['werkzueg_filter_extenstions_callback']


def werkzueg_filter_extenstions_callback(record):
    extensions_to_filter = getattr(settings, 'WERKZUEG_FILTER_EXTENSTIONS', False)
    if extensions_to_filter:
        return not any(['.{0}'.format(ext) in record.msg for ext in extensions_to_filter])
    else:
        return True
