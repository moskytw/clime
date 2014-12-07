#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

try:
    bytes
except NameError:
    bytes = str
    str = unicode

def reverse(x):
    '''We assume it is a helper function for something else.

    It returns True to let other stuff work.
    '''

    if not isinstance(x, (bytes, str)):
        x = str(x)

    if isinstance(x, bytes):
        x = x.decode('utf-8')

    print(x[::-1])

    return x

if __name__ == '__main__':
    import clime
    clime.start(ignore_return=True, debug=True)
