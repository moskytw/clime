#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import *

sys.argv[0] = 'clime'

def clime(target, *args):
    '''Dynamicly make a module or Python file into CLI program.

    `target` can be a moudle or Python file path.'''

    module = None

    try:
        module = __import__(target)
    except ImportError:
        pass

    try:
        module = {}
        execfile(target, module)
    except IOError, e:
        module = None
        print '%s: %s' % (sys.argv[0], e)

    if module:
        prog = Program(module)
        prog(sys.argv[2:])

main({'clime': clime})
