#!/usr/bin/env python
# -*- coding: utf-8 -*-

def hello():
    '''Just print Hello for you.'''

    print 'Hello!'

def echo(string):
    '''Print string by return value.'''

    return string

def repeat(string, times=2):
    '''Repeat a string by n times.
    
    Options:
        -n, --times  Repeat n times. Default is 2 times.'''

    for i in range(times):
        print string

repeat.aliases = {'n': 'times'}


if __name__ == '__main__':
    import clime
    clime.main()
