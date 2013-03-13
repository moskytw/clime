#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import imp
from .program import Program

sys.argv[0] = 'clime'

def clime(target, *args, **kargs):
    '''Make a module or Python file into CLI program.

    `target` can be a moudle or Python file path.'''

    module = None

    try:
        module = __import__(target)
    except ImportError:
        module = imp.load_source('tmp', target)

    prog = Program(module)
    prog.main(sys.argv[2:])
