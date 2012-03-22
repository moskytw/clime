Clime
=====

Clime is a simple Python module to let you convert a Python program contains
functions into a multi-command CLI program.

See the full documentaion on http://docs.mosky.tw/clime/ .

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

CLI-ize ME!
-----------

Here is the basic usage of Clime.

You have two different ways to use Clime.

1. **Insert Lines into Source**
   
   Just add two lines below into your source ::
   
     import clime
     clime.main()
   
   Recommend to put the codes into the ``if __name__ == '__main__':`` block.

2. **Use clime.py as A Command**
   
   `clime.py` is also an executable script. Use it to convert a moudle temporarily.
   
   For convenience, make a command for `clime.py` ::
   
     $ sudo ln -s /usr/local/lib/python<VERSION>/dist-packages/clime.py /usr/bin/clime
     $ sudo chmod 755 /usr/bin/clime 
     
   Then, you can use ``clime`` as a normal command ::

     $ clime <module_name> <args_for_module>

Examples
""""""""

Here is a example of a script uses Clime:

::

    # file: example/singlecmd.py

    '''Here is docstring of module.'''

    def onlyme(s, b=True, l=None):
        '''Here is docstring of function.'''

        print 's:', s
        print 'b:', b
        print 'l:', l

    if __name__ == '__main__':
        import clime
        clime.main()

After added the last 2 lines, this script is a CLI program now. Try to use
it on shell.

1. Call the program with `--help` ::

    $ python singlecmd.py --help
    usage: singlecmd.py [-b] [-l VAL] s 
       or: singlecmd.py onlyme [-b] [-l VAL] s 

    Here is docstring of module.

2. Call the program with `Command` and `--help` ::

    $ python singlecmd.py onlyme --help
    usage: singlecmd.py onlyme [-b] [-l VAL] s 

    Here is docstring of function.

3. The different behaviors decide by default value ::

    $ python singlecmd.py test -b -loption_arg
    s: test
    b: False
    l: option_arg

4. Duplicate options ::

    $ python singlecmd.py test -bbb -l one -l two -l three
    s: test
    b: 3
    l: ['one', 'two', 'three']

See the `clime.Command.parse`_ section for more details
about argument parsing.

More examples are in the `clime/examples`_.

The basic usage of Clime is end here. If you want to know more details or
help Clime, please visit `Take a Deeper Look at Clime`_.

.. _`clime.Command.parse`:
    http://docs.mosky.tw/clime/deeper.html#clime.Command.parse

.. _`clime/examples`:
    https://github.com/moskied/clime/tree/master/examples

.. _`Take a Deeper Look at Clime`:
    http://docs.mosky.tw/clime/deeper.html
