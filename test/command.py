#!/usr/bin/env python
# -*- coding: utf-8 -*-

from clime import Command

def repeat(s, time=2, debug=False):
    '''repeat s n times

    -t N, --time N   repeat N times.
    -d, --debug      for dubug'''

    print s * time

if __name__ == '__main__':

    from math import hypot, log

    repeat_cmd = Command(repeat)

    s = '-t 1 -t2 -t=3 --time 4 --time=5 hey1 -dddd hey2'
    print s
    print repeat_cmd.scan(s)
    print repeat_cmd.usage()

    hypot_cmd = Command(hypot)

    s = '3 4'
    print hypot_cmd.scan(s)
    print hypot_cmd.usage()

    log_cmd = Command(log)

    s = '10'
    print log_cmd.scan(s)
    print log_cmd.usage()
