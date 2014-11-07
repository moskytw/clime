The Changes
===========

v0.2.7
------

1. It now generates metavar for argument which has default value.
2. Fixed argument whose default is bool took next command line argumnet as its
   value. (``--bool shouldnttake``)
3. Fixed it caught option-like string in option description.
4. Refactored the :meth:`~clime.core.Command.parse`.

v0.2.6
------

1. Make the setup.py better.
2. Refactored the :mod:`clime.__main__`.
3. Refactored the :mod:`clime.now`.

v0.2.5
------

1. Renamed the :meth:`~clime.core.Command.get_usage` to
   :meth:`~clime.core.Command.build_usage`.
2. Refactored the code and the doc.

v0.2.4
------

1. Fixed a bug of finding docstring of command.
2. Added support for using ``f`` and ``float`` as metavar in docstring. Thanks
   for the contribution from `mail6543210
   <https://github.com/moskytw/clime/pull/18>`_.

v0.2.3
------

1. It now shows the doc of program only if the object is a module
2. It is also a command now. You can use ``clime`` from shell.

v0.2.2
------

1. It now prints the doc of default command if doc of program is not available.

v0.2.1
------

1. Fixed the bug of program name.

v0.2
----

1. It now catches more exceptions (include KeyboardInterrupt).
2. Added :func:`clime.core.start` which works equally as
   :func:`clime.core.customize`

v0.1.9
------

1. Added :attr:`clime.core.CMD_SUFFIX` and an argument, `white_pattern`, for
   :class:`clime.core.Program`.

v0.1.8
------

1. It now exits with 1 if there has error -- issue `#14
   <https://github.com/moskytw/clime/issues/14>`_.

v0.1.7
------

1. Fixed the bug with generator -- issue `#12
   <https://github.com/moskytw/clime/issues/12>`_.

v0.1.6
------

1. It now supports the `ignore_return` in :py:class:`~clime.core.Program` class.
2. Added a shortcut, :py:func:`~clime.core.customize`, of using Program class.
3. Fixed the support of the ``-kmeta`` format in docstring.

v0.1.5
------

1. It now uses `<meta>` instead of `META`.
2. It supports more metavars, include `<json>` for the string in json format.
3. It supports more options of creating a program, include `white_list`,
   `black_list`, `ignore_help`, `debug`, ...
4. It repects `__all__` now.
5. Refactored the code a lot and the whole file structure.

