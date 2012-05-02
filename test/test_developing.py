#!/usr/bin/env python
# -*- coding: utf-8 -*-

from clime import *
from clime.helper import parse

def repeat(s, times=10):
    ''' Repeat a string n times.
    
    -t, --times  repeat n times.'''
    return x, y

if __name__ == '__main__':

    print parse('--long first --long second -m string --long=string -s1 -s -s 2 -s=3', {}, ['-m'])

    p = Parser(repeat)
    print p.parse('string -t -t 123 ')

