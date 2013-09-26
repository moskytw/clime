The API of Clime
================

The ``clime.now`` Class
-----------------------

It is the simplest way to convert your module into a CLI program:

::

    import clime.now

Actually, this module is equal to execute:

::

    from clime import Program
    prog = Program()
    prog.main()

.. seealso::
    The :py:class:`~clime.core.Program` class provides many options to customize
    your program. It may be a good idea to take a look.

The ``clime.__main__`` Moudle
-----------------------------

.. automodule:: clime.__main__
    :members:

The ``clime.core`` Module
-------------------------

.. automodule:: clime.core
    :members:

The ``clime.util`` Module
-------------------------

.. automodule:: clime.util
    :members:

The ``clime.__main__`` Moudle
=============================

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
