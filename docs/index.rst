.. Clime documentation master file, created by
   sphinx-quickstart on Mon Mar 19 21:47:40 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Introduction
============

Clime let you convert a module, a dict or an instance into a multi-command
CLI program.

It just scans the members of an object to find the functions out, so it is
**low couple** with your source. It also scans the aliases and metavars of
options from docstring, so you are free from writing the settings of
options. You can focus on writing the help text of your CLI program.

It is a better choice than the heavy `optparse` or `argparse` for simple CLI
tasks.

Let me show an example for you.

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

After add this line, ::

    import clime.now

... you now have a CLI program! ::
    
    $ python repeat.py twice
    twicetwice

    $ python repeat.py -n3 thrice
    thricethricethrice

And it gerneate the usage from your function: ::

    $ python repeat.py --help
    usage: [--time N | -n N] STRING
       or: repeat [--time N | -n N] STRING

If you wrote a docstring, it will also show up in help text. ::

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
    https://github.com/moskied/clime/tree/master/examples

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
   
     $ git clone git://github.com/moskied/clime.git
     
   to clone a Clime repository. Or download manually from GitHub_.

.. _GitHub:
    http://github.com/moskied/clime

.. _PyPI:
    http://pypi.python.org/pypi/clime

Usage
-----

Here is the basic usage of Clime.

You have two different ways to use Clime.

1. **Insert A Line into Your Source**
   
   Just add this line into your source ::
   
     import clime.now
   
   It is recommend to put the codes into the ``if __name__ == '__main__':`` block.

2. **Use Clime as A Command**
   
   `clime` is also an executable module. Use it to convert a module or a
   Python file temporarily. ::
   
     $ python -m clime TARGET

.. seealso::
    :func:`clime.Program` for more usages.

More Details
------------

These are the basics of Clime usage. If you want to know more, details are
here:

.. toctree::
   :maxdepth: 2

   deeper

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

