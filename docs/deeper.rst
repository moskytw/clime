Take a Deeper Look at Clime
===========================

This page contains the many details of Clime. If you just want to use Clime, you can
skip this page.

What Happens after `clime.main()`
--------------------------------

When ``clime.main()`` is called, Clime gets the '__main__' module in
``sys.modules`` and scans the functions in it. Then it converts them into
:class:`.Command` objects.

Clime takes the first argument as a command name. Clime finds the command by name
and calls that command.

Introducing the Classes
---------------------

`clime` has two main classes, :class:`.Command` and :class:`.Program`.

Class `Command` allows a function, built-in function or bound method to
accept arguments from the command line. Class `Program` scans the attributes
in an object or a dict and then turns it into a CLI program.

The two classes are callable. You can call them with the command-line-style arguments.

The API of Clime
----------------

.. automodule:: clime
    :members:
    :undoc-members:
