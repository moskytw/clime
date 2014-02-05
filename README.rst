.. image:: https://travis-ci.org/moskytw/clime.png
   :target: https://travis-ci.org/moskytw/clime

.. image:: https://pypip.in/v/clime/badge.png
   :target: https://pypi.python.org/pypi/clime

.. image:: https://pypip.in/d/clime/badge.png
   :target: https://pypi.python.org/pypi/clime

The full version of this documentaion is at `clime.mosky.tw
<http://clime.mosky.tw>`_.

Clime
=====

Clime lets you convert any module into a multi-command CLI program without any
configuration.

The main features:

1. It works well with zero configuration. Free you from the configuration hell.
2. Docstrings (i.e., help texts) is just configurations. When you finish a
   docstring, a configuration of aliases and metavars are also finished.
3. It generates usages for each command automatically.

It is a better choice than the heavy optparse or argparse for most of the CLI
tasks.

CLI-ize ME!
-----------

Let me show you Clime with an example.

Here we have a simple script with a docstring here: ::

    # file: repeat.py

    def repeat(message, times=2, count=False):
        '''It repeats the message.

        options:
            -m=<str>, --message=<str>  The description of this option.
            -t=<int>, --times=<int>
            -c, --count
        '''

        s = message * times
        return len(s) if count else s

After add this line: ::

    import clime.now

`clime.now <http://clime.mosky.tw/api.html#module-clime.now>`_ describes more
about how to customize your program.

... your CLI program is ready! ::

    $ python repeat.py twice
    twicetwice

    $ python repeat.py --times=3 thrice
    thricethricethrice

It also generates a pretty usage for this script: ::

    $ python repeat.py --help
    usage: [-t<int> | --times=<int>] [-c | --count] <message>
       or: repeat [-t<int> | --times=<int>] [-c | --count] <message>

If you have a docstring in your function, it also shows up in usage manual with
``--help``. ::

    $ python repeat.py repeat --help
    usage: [-t<int> | --times=<int>] [-c | --count] <message>
       or: repeat [-t<int> | --times=<int>] [-c | --count] <message>

    It repeats the message.

    options:
        -m=<str>, --message=<str>  The message.
        -t=<int>, --times=<int>
        -c, --count

You can find more examples in the `clime/examples`_.

`.Command <http://clime.mosky.tw/api.html#clime.core.Command>`_ describes more
about how it works.

.. _`clime/examples`:
    https://github.com/moskytw/clime/tree/master/examples

Installation
------------

Clime is hosted on two different platforms, PyPI_ and GitHub_.

Install from PyPI
~~~~~~~~~~~~~~~~~

Install Clime from PyPI_ for a stable version: ::

    $ sudo pip install clime

If you don't have pip, execute ::

    $ sudo apt-get install python-pip

to install pip on Debian-base Linux distribution.

Get Clime from GitHub
~~~~~~~~~~~~~~~~~~~~~

If you want to follow the latest version of Clime, use ::

    $ git clone git://github.com/moskytw/clime.git

to clone a Clime repository, or download manually from GitHub_.

.. _GitHub:
    http://github.com/moskytw/clime

.. _PyPI:
    http://pypi.python.org/pypi/clime
