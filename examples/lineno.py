#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

def lineno(start=0):
    for i, line in enumerate(sys.stdin, start):
        sys.stdout.write('%3d| %s' % (i, line))

if __name__ == '__main__':
    import clime.now
