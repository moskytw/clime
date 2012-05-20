#!/usr/bin/env python
# -*- coding: utf-8 -*-

from clime import ArgSpec

def repeat(s, time=2, debug=False):
    '''repeat s n times

    -t, --time   repeat n times.'''

    print s * time

if __name__ == '__main__':
    argspec = ArgSpec(repeat)

    print argspec.args
    print argspec.defaults
    print argspec.bindings
