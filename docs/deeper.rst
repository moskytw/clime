Take a Deeper Look at Clime
===========================

This page contains the details of Clime. If you just want to use Clime, you
can skip this page.

About ``import clime.now``
--------------------------

The content in `clime.now` is roughly same as: ::

    from clime import Program
    Program().main()

If you want to customize the CLI program, see :class:`.Program` for more
details.

Options in Docstring
--------------------

The class, :class:`.Command`, will scan the options and metavars in
docstring.

The lines match the following regex will be picked. ::

    r'*(-.+?) {2,}'

Then Clime will use this regex to find out options and metavars in picked
lines. ::

    r'''--?({0}) # option
       (?:
          \[?
          [= ]
          ({0})  # metavar
       )?
       ,?
    ''' \
   .format('[^\s,=\[\]]+')

Some examples: ::

    -d, --debug                enable debug mode
    -q, -s, --quiet, --slient  enable slient mode
    -n N, --times N            how many times do you want

Meta Variables
--------------

A meta variable also represent the type. By default, `N`, `NUM` is ``int``.
You can add the mapping of metavar and the type at
:attr:`.Command.metatypes`.

Introducing the Classes
-----------------------

Clime has two main classes, :class:`.Command` and :class:`.Program`.

Class `Command` makes a function, built-in function or bound method accpects
the argument from command line. Class `Program` scans the attributes in an
object or a dict and make them into a CLI program.

The API of Clime
----------------

.. autoclass:: clime.Program
    :members:
    :undoc-members:

.. autoclass:: clime.Command
    :members:
    :undoc-members:

.. automodule:: clime.helper
    :members:
