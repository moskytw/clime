Take a Deeper Look at Clime
===========================

This page contains the many details of Clime. If you just want to use, you can
skip this page.

What Happen after `clime.main()`
--------------------------------

When ``clime.main()`` is called, Clime gets the '__main__' module in
``sys.modules`` and scans the functions in it.

Next, Clime takes the first argument as function name to find the function
in this module.

Finally, Clime convert this function into `Command` object and call it with
the arguments.

Introduce the Classes
---------------------

`clime` has two main classes, `Command <#clime.Command>`_ and `Program
<#clime.Program>`_.

Class `Command` makes a function or callable object to accpect the argument
from command line. Class `Program` scans the attributes in an object and
make this object into a CLI program.

Two classes are callable. You can call them with the command-line-style argument.

The API of Clime
----------------

.. automodule:: clime
    :members:
    :undoc-members:
