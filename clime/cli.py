#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from .program import Program

sys.argv[0] = 'clime'

def clime(target, *args, **kargs):
    '''Dynamicly make a module or Python file into CLI program.

    `target` can be a moudle or Python file path.'''

    module = None

    try:
        module = __import__(target)
    except ImportError:

        try:
            module = {}
            execfile(target, module)
        except IOError, e:
            print >> sys.stderr, 'clime: %s' % e
            return

    if module is not None:
        prog = Program(module)
        prog.main(sys.argv[2:])
    else:
        assert 'something wrong. you should not go here.'
