#!/usr/bin/env python
# -*- coding: utf-8 -*-

from clime import *

def repeat(s, times=10):
    ''' Repeat a string n times.
    
    -t, --times  repeat n times.'''
    return x, y

if __name__ == '__main__':

    p = Parser(repeat)
    print p.parse('string --times 10')
    print p.parse('string --times=10')
    print p.parse('string -t10')
    print p.parse('string -t 10')
    print p.parse('string -t=10')

