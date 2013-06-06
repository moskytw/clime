#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Clime is also an *executable* module.

Use ``python -m clime`` to execute any module or Python file as a CLI program.

Here are the examples:

::

    $ python -m clime math
    usage: acos [-x] <x>
       or: acosh [-x] <x>
       or: asin [-x] <x>
       or: asinh [-x] <x>
       or: atan [-x] <x>
    ...

    $ python -m clime math hypot --help
    usage: hypot [-x] [-y] <x> <y>

    hypot(x, y)

    Return the Euclidean distance, sqrt(x*x + y*y).

    $ python -m clime math hypot 3 4
    5.0
'''

import sys
import imp
from .core import Program

sys.argv[0] = 'clime'

def clime(target, *args, **kargs):

    module = None

    try:
        module = __import__(target)
    except ImportError:
        module = imp.load_source('tmp', target)

    prog = Program(module)
    prog.main(sys.argv[2:])

def main():
    Program({'clime': clime}, ignore_help=True).main()

if __name__ == '__main__':
    main()

