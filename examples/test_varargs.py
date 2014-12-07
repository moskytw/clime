#!/usr/bin/env python
# -*- coding: utf-8 -*-

def repeat(message, times=2, count=False, *args, **kargs):
    '''It repeats the message.

    options:
        -m=<str>, --message=<str>  The description of this option.
        -t=<int>, --times=<int>
        -c, --count
    '''
    print args, kargs
    s = message * times
    return len(s) if count else s

if __name__ == '__main__':
    import clime
    clime.start(debug=True)
