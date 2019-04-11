from slugify import slugify

__all__ = ['urlify']


def urlify(value):
    """
    This is small wrapper for `slugify`. Original function can be used:

        from slugify import slugify

    Example usage:

        from baseapp.utils import urlify

        corrected_text = urlify('Merhaba Dünya!')

    >>> urlify('Merhaba Dünya')
    'merhaba-dunya'

    >>> urlify('Uğur Özyılmazel')
    'ugur-ozyilmazel'

    >>> urlify('çğüÇ ĞÜıİ')
    'cguc-guii'

    """

    return slugify(value)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
