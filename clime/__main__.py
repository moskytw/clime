#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import imp
from .core import Program, start

def convert(target, *args, **kargs):

    module = None

    try:
        module = __import__(target)
    except ImportError:
        module = imp.load_source('tmp', target)

    prog = Program(module)
    prog.main(sys.argv[2:])

# This function is used by the command script installed in system.
def run():
    sys.argv[0] = 'clime'
    start({'convert': convert})

if __name__ == '__main__':
    # ``python -m clime`` will go here.
    run()
