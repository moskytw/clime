#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''It is the simplest way to convert your module into a CLI program:

::

    import clime.now

Actually, this module is equal to execute:

::

    from clime import Program
    prog = Program()
    prog.main()

The :py:class:`~clime.core.Program` class provides many options to customize
your program. It may be a good idea to take a look.

'''

from .core import Program

Program().main()
