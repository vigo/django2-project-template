__all__ = [
    'numerify',
]


def numerify(input, default=-1):
    """ (number or string, default=-1) -> number

    This is good for query string operations.

    >>> numerify(1)
    1
    >>> numerify("1")
    1
    >>> numerify("1a")
    -1
    >>> numerify("ab")
    -1
    >>> numerify("abc", default=44)
    44
    """

    if str(input).isnumeric():
        return int(input)
    return default


if __name__ == '__main__':
    import doctest
    doctest.testmod()
