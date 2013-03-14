#!/usr/bin/env python
# -*- coding: utf-8 -*-

def repeat(message, times=2, count=False):
    '''It repeat the message.

    options:
        -m=<str>, --message=<str>  The message.
        -t=<int>, --times=<int>
        -c, --count
    '''

    s = message * times
    return len(s) if count else s

if __name__ == '__main__':
    import clime.now
