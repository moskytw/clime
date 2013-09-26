#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sys import getfilesystemencoding as _getfilesystemencoding

ENCODING = _getfilesystemencoding()

def reverse(x):
    '''We assume it is a helper function for something else.

    It returns True to let other stuff work.
    '''

    if not isinstance(x, basestring):
        x = unicode(x)

    if isinstance(x, str):
        x = unicode(x, ENCODING)

    print x[::-1].decode(ENCODING)

    return x

if __name__ == '__main__':
    import clime
    clime.start(ignore_return=True)
