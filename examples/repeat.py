#!/usr/bin/env python
# -*- coding: utf-8 -*-

def repeat(string, time=2):
    '''repeat string n times

    options:
        -n N, --time N  repeat N times.
    '''

    print string * time

if __name__ == '__main__':
    import clime.now
