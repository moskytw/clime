#!/usr/bin/env python
# -*- coding: utf-8 -*-

def repeat(message, times=2, count=False):
    '''It repeats the message.

    options:
        -m=<str>, --message=<str>  The message you want to repeat.
        -t=<int>, --times=<int>    How many times?
        -c, --count                Count it?
    '''

    s = message * times
    return len(s) if count else s

if __name__ == '__main__':
    import clime.now
