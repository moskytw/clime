The Shortcuts of Clime
======================

.. py:module:: clime.now

It is the simplest way to convert your module into a CLI program:

::

    import clime.now

The above line is same as to execute:

::

    import clime
    clime.start()

In this form, you can pass arguments to :func:`~clime.core.start` to customize your CLI program.

The most formal way is:

::

    from clime import Program
    prog = Program()
    prog.main()

The only case to use this form is you want to customize arguments for your CLI
program. You can do it by passing arguments to :meth:`~clime.core.Program.main`.

The Core Module --- ``clime.core``
==================================

.. testsetup::

    from clime.core import Command

.. automodule:: clime.core
    :members:

The Utility Module --- ``clime.util``
=====================================

.. automodule:: clime.util
    :members:

Run Clime as a Command
======================

.. py:module:: clime.__main__

Clime lets you use ``python -m clime`` or ``clime`` in shell to converts a
Python program or Python module temporarily.

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
