#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''It is a standard example for Clime.'''

def hello():
    '''Just print Hello for you.'''

    print 'Hello!'

def echo(string):
    '''Print string by return value.'''

    return string

def repeat(string, times=2):
    '''Repeat a string by n times.
    
    Options:
        -n NUM, --times NUM  Repeat n times. Default is 2 times.'''

    for i in range(times):
        print string

repeat.aliases = {'n': 'times'}

def summary(line=2, *paths):
    '''Summary files.

    Options:
        -n NUM, --line NUM   How many lines do you want to show?'''

    for path in paths:
        print path+':'
        try:
            f = open(path)
        except IOError, e:
            print e
        else:
            for i in range(line):
                print f.readline()
        print

summary.aliases = {'n': 'line'}

if __name__ == '__main__':
    import clime
    clime.main()
