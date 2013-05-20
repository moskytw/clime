#!/usr/bin/env python
# -*- coding: utf-8 -*-

def reverse(string):
    '''reverse string
    '''

    print string.decode('UTF-8')[::-1]

if __name__ == '__main__':

    # > v0.2
    import clime
    clime.start(ignore_return=True)

    # >= v0.1.6
    #import clime
    #clime.customize(ignore_return=True)

    # It also works, because the ``reverse`` returns noting.
    #import clime.now
