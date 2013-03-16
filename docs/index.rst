.. Clime documentation master file, created by
   sphinx-quickstart on Mon Mar 19 21:47:40 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Introduction
============

Clime lets you convert *any* module into a multi-command CLI program *without*
any configuration.

Here is a slide which introduces you to Clime:

.. raw:: html

    <iframe src="http://www.slideshare.net/slideshow/embed_code/17237148" width="597" height="486" frameborder="0" marginwidth="0" marginheight="0" scrolling="no" style="border:1px solid #CCC;border-width:1px 1px 0;margin-bottom:5px" allowfullscreen webkitallowfullscreen mozallowfullscreen> </iframe> <div style="margin-bottom:5px"> <strong> <a href="http://www.slideshare.net/moskytw/clime" title="Introduction to Clime" target="_blank">Introduction to Clime</a> </strong> from <strong><a href="http://www.slideshare.net/moskytw" target="_blank">Mosky Liu</a></strong> </div>

The main features:

1. It works well with *zero* configuration. Free you from the configuration hell.
2. Docstring just *is* config. When you finish the docstring, the config of the
   aliases and metavars are also finished.
3. Auto-generate the usage of each command from the functions.

It is a better choice than the heavy `optparse` or `argparse` for most of the
CLI tasks.

Let me show you Clime with an example.

CLI-ize ME!
-----------

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

By adding this line, ::

    import clime.now

... your CLI program is ready! ::
    
    $ python repeat.py twice
    twicetwice

    $ python repeat.py --times=3 thrice
    thricethricethrice

And it generates the usage manual: ::

    $ python repeat.py --help
    usage: [-t<int> | --times=<int>] [-c | --count] <message>
       or: repeat [-t<int> | --times=<int>] [-c | --count] <message>

If you have a docstring in your function, it also show up in usage manual with
``--help``. ::

    $ python repeat.py repeat --help
    usage: [-t<int> | --times=<int>] [-c | --count] <message>
       or: repeat [-t<int> | --times=<int>] [-c | --count] <message>

    It repeat the message.

    options:
        -m=<str>, --message=<str>  The message.
        -t=<int>, --times=<int>
        -c, --count
    
You can find more examples in the `clime/examples`_.

.. seealso::
    This page, :py:meth:`.Command.parse`, describes how Clime parses the
    arguments.

.. seealso::
    If you are interesting in the aliases or the metavariables which Clime
    provides, read :py:class:`~clime.core.Command` for more infomation.

.. _`clime/examples`:
    https://github.com/moskytw/clime/tree/master/examples

Installation
------------

Clime is hosted on two different platforms, PyPI_ and GitHub_.

1. **Install from PyPI**
   
   Install Clime from PyPI_ for a stable version ::
   
     $ sudo pip install clime
     
   If you don't have `pip`, execute ::
   
     $ sudo apt-get install python-pip
     
   to install `pip` on Debian-base Linux distribution.

2. **Get Clime from GitHub**
   
   If you want to follow the lastest version of Clime, use ::
   
     $ git clone git://github.com/moskytw/clime.git
     
   to clone a Clime repository. Or download manually from GitHub_.

.. _GitHub:
    http://github.com/moskytw/clime

.. _PyPI:
    http://pypi.python.org/pypi/clime

Usage
-----

Below illustrates the basic usage of Clime.

You have two different ways to use Clime.

1. **Insert A Line into Your Source**
   
   Just add this line into your source ::
   
     import clime.now
   
   It is recommended to put the line in the ``if __name__ == '__main__':``
   block.

2. **Use Clime as A Command**
   
   `clime` is also an executable module. You can use it to convert a module or a
   stand-alone program temporarily. ::
   
     $ python -m clime TARGET

.. seealso::
    If you want to know how to customize the program, read :py:class:`.Program`
    for more infomation.

More Details
------------

There are just the basic usage of Clime. If you want to know more, details are
listed here:

.. toctree::
    :maxdepth: 2

    api

The Changes
-----------
   
.. toctree::
    :maxdepth: 2

    changes

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

