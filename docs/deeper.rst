Take a Deeper Look at Clime
===========================

This page contains the many details of Clime. If you just want to use, you can
skip this page.

What Happen after `clime.main()`
--------------------------------

When ``clime.main()`` is called, Clime gets the '__main__' module in
``sys.modules`` and scans the functions in it. And converts them into
:class:`.Command` objects.

Then, Clime takes the first argument as command name. Find the command out
and call that command.

Introduce the Classes
---------------------

`clime` has two main classes, :class:`.Command` and :class:`.Program`.

Class `Command` makes a function, built-in function or bound method to
accpect the argument from command line. Class `Program` scans the attributes
in an object or a dict and make that into a CLI program.

Two classes are callable. You can call them with the command-line-style argument.

The API of Clime
----------------

.. automodule:: clime
    :members:
    :undoc-members:
