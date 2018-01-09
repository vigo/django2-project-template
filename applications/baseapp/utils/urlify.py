LETTER_TRANSFORM_MAP = {
    'tr': {
        'ç': 'c',
        'Ç': 'c',
        'ğ': 'g',
        'Ğ': 'g',
        'ı': 'i',
        'I': 'i',
        'İ': 'i',
        'ö': 'o',
        'Ö': 'o',
        'ş': 's',
        'Ş': 's',
        'ü': 'u',
        'Ü': 'u',
    },
}


__all__ = [
    'urlify',
]


def urlify(value, language='tr'):
    """
    This is a pre-processor for django's slugify function.

    Example usage:

        from django.utils.text import slugify

        corrected_text = slugify(urlify('Merhaba Dünya!'))

    >>> urlify('Merhaba Dünya')
    'merhaba dunya'

    >>> urlify('Uğur Özyılmazel')
    'ugur ozyilmazel'

    >>> urlify('ç ğ ü Ç Ğ Ü ı İ')
    'c g u c g u i i'

    """

    return ''.join(map(lambda char: LETTER_TRANSFORM_MAP[language].get(char, char), iter(value))).lower()


if __name__ == '__main__':
    import doctest
    doctest.testmod()
