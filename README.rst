Clime
=====

Clime is a Python module to let you convert a Python program contains
functions into a multi-command CLI program.

Clime is *very easy* to use and *low couple* (even not!) with your source.
It is a better choice than the heavy `optparse` or `argparse` for simple CLI
tasks. 

Let me show an example for you.

See the full documentaion on http://docs.mosky.tw/clime/ .

CLI-ize ME!
-----------

A simple script here: ::

    #file: test.py
    def repeat(string, n=2):
        for i in range(n):
            print string

After add two lines, ::

    import clime
    clime.main()

... you have a CLI program now! ::
    
    $ python test.py twice
    twice
    twice

    $ python test.py -n3 thrice
    thrice
    thrice
    thrice

And it also support ``--help``: ::

    usage: test.py [-n VAL] STRING 
       or: test.py repeat [-n VAL] STRING

If you wrote the docstring, it will also show on help.
    
You can find more examples in the `clime/examples`_.

See `clime.Command.parse`_ for more details about argument parsing.

.. _`clime/examples`:
    https://github.com/moskied/clime/tree/master/examples
    
.. _`clime.Command.parse`:
    http://docs.mosky.tw/clime/deeper.html#clime.Command.parse

Installation
------------

Clime is hosted on two different platform, PyPI_ and GitHub_.

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

1. **Insert Lines into Source**
   
   Just add two lines below into your source ::
   
     import clime
     clime.main()
   
   Recommend to put the codes into the ``if __name__ == '__main__':`` block.

2. **Use clime.py as A Command**
   
   `clime.py` is also an executable script. Use it to convert a moudle or a
   Python file temporarily.
   
   For convenience, make a command for `clime.py` ::
   
     $ sudo ln -s /usr/local/lib/python<VERSION>/dist-packages/clime.py /usr/local/bin/clime
     $ sudo chmod 755 /usr/local/bin/clime 
     
   Then, you can use ``clime`` as a normal command ::

     $ clime MODULE_OR_FILE ARGS

   See `clime.main`_ for more usages.
    
.. _`clime.main`:
    http://docs.mosky.tw/clime/deeper.html#clime.main

More Details
------------

It is the all of basic of Clime. If you want to know more, please visit `Take a Deeper Look at Clime`_.

.. _`Take a Deeper Look at Clime`:
    http://docs.mosky.tw/clime/deeper.html
