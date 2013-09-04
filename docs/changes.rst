
The Changes
===========

v0.2.4
------

1. fixed a bug of finding docstring of command.
2. added support of use ``f`` and ``float`` in docstring. Thanks for the
   contirbution from `mail6543210 <https://github.com/moskytw/clime/pull/18>`_.

v0.2.3
------

1. show the doc of program only if the object is a module
2. Clime is also a command now. You can use ``clime`` from shell.

v0.2.2
------

1. print the doc of default command if doc of program is not available

v0.2.1
------

1. fixed the bug of program name

v0.2
----

1. catch more exceptions (include KeyboardInterrupt)
2. added :func:`clime.core.start` which works equally as :func:`clime.core.customize`

v0.1.9
------

1. added :attr:`clime.core.CMD_SUFFIX` and an argument, `white_pattern`, for :class:`clime.core.Program`.

v0.1.8
------

1. exits with 1 if there has error -- issue `#14 <https://github.com/moskytw/clime/issues/14>`_.

v0.1.7
------

1. fixed the bug with generator -- issue `#12 <https://github.com/moskytw/clime/issues/12>`_.

v0.1.6
------

1. supports the `ignore_return` in :py:class:`~clime.core.Program` class.
2. added the a shortcut, :py:func:`~clime.core.customize`, of using Porgram class.
3. fixed the support of the ``-kmeta`` format in docstring.

v0.1.5
------

1. uses `<meta>` instead of `META`.
2. supports more metavars, include `<json>` for the string in json format.
3. supports more options of creating a program, include `white_list`,
   `black_list`, `ignore_help`, `debug`, ...
4. repects `__all__` now.
5. refactored the code a lot and the whole file structure.

