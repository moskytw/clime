#!/usr/bin/env python
# -*- coding: utf-8 -*-

from math import log, hypot

def repeat(string, time=2, debug=False):
    '''repeat s n times

    options:
        -t N, --time N   repeat N times.
        -d, --debug      for dubug'''

    print string * time

if __name__ == '__main__':
    import clime.now
