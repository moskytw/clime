The Shortcuts of Clime
======================

.. py:module:: clime.now

It is the simplest way to convert your module into a CLI program:

::

    import clime.now

This module is a shortcut to execute:

::

    import clime
    clime.start()

The :func:`~clime.core.start` is still a shortcut, but it allows you to give arguments
to customize.

The most formal way is:

::

    from clime import Program
    prog = Program()
    prog.main()

You won't want to use this way, except to modify the argument from system. The
:meth:`~clime.core.Program.main` accepts the command line arguments. If nothing
passes in, it simply finds the arguments in ``sys.argv``.

The Core Module --- ``clime.core``
==================================

.. automodule:: clime.core
    :members:

The Utility Module --- ``clime.util``
=====================================

.. automodule:: clime.util
    :members:

Run Clime as a Command
======================

.. py:module:: clime.__main__

This module lets you use ``python -m clime`` or ``clime`` to converts a Python
program or Python module from shell.

Here are some examples:

.. code-block:: bash

    $ python -m clime math
    usage: acos [-x] <x>
       or: acosh [-x] <x>
       or: asin [-x] <x>
       or: asinh [-x] <x>
       or: atan [-x] <x>
    ...

.. code-block:: bash

    $ python -m clime math hypot --help
    usage: hypot [-x] [-y] <x> <y>

    hypot(x, y)

    Return the Euclidean distance, sqrt(x*x + y*y).

.. code-block:: bash

    $ python -m clime math hypot 3 4
    5.0
