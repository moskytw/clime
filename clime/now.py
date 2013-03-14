#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''It let you convert you moudle in one line.

::
    if __name__ == '__main__':
        import clime.now

If your file run as a top-level moudle, it triggers Clime to convert your
moudle.
'''

from .core import Program

Program().main()
