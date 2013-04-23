The API of Clime
================

The ``clime.now`` Class
-----------------------

.. .. NOTE: It can't be automodule.
.. .. automodule:: clime.now
..     :members:

It is the simplest way to convert your module into a CLI program:

::

    import clime.now

Actually, this module is equal to execute:

::

    from clime import Program
    prog = Program()
    prog.main()

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
