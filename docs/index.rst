.. Clime documentation master file, created by
   sphinx-quickstart on Mon Mar 19 21:47:40 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Introduction
============

Clime lets you convert a module, a dict or an instance into a multi-command
CLI program.

It scans the members of an object to find the functions out, so it is
**low couple** with your source. It also scans the aliases and metavars of
options from docstring, so you are free from writing the settings of
options. You can focus on writing the help text of your CLI program.

It is a better choice than the heavy `optparse` or `argparse` for simple CLI
tasks.

Let me show you Clime with an example.

.. note::
    The 0.1.4 is a rewrote version and it does **not** provide backward
    compatibility.

CLI-ize ME!
-----------

Here we have a simple script with docstring here: ::

    # filename: repeat.py
    
    def repeat(string, time=2):
        '''repeat string n times

        options:
            -n N, --time N  repeat N times.
        '''
        
        print string * time

By adding this line, ::

    import clime.now

... your CLI program is ready! ::
    
    $ python repeat.py twice
    twicetwice

    $ python repeat.py -n3 thrice
    thricethricethrice

And it generates the usage manual from the docstring your function: ::

    $ python repeat.py --help
    usage: [--time N | -n N] STRING
       or: repeat [--time N | -n N] STRING

If you have a docstring in your function, it also show up in usage manual with '--help'. ::

    $ python repeat.py repeat --help
    usage: [--time N | -n N] STRING
       or: repeat [--time N | -n N] STRING

    repeat string n times

    options:
        -n N, --time N  repeat N times.
    
You can find more examples in the `clime/examples`_.

.. seealso::
   :meth:`.Command.scan` for more details about argument parsing.

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
   
   It is recommended to put the line in the ``if __name__ == '__main__':`` block.

2. **Use Clime as A Command**
   
   `clime` is also an executable module. You can use it to convert a module or a stand-alone program temporarily. ::
   
     $ python -m clime TARGET

.. seealso::
    :func:`clime.Program` for more usages.

More Details
------------

These are the basics of Clime usage. If you want to know more, details are listed here:

.. toctree::
   :maxdepth: 2

   deeper

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

