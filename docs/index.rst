.. Clime documentation master file, created by
   sphinx-quickstart on Mon Mar 19 21:47:40 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Clime's documentation!
=================================

This is the documentaion of Clime.

Clime is a simple Python module to let you convert a Python program contains
functions into a multi-command CLI program.

Installation
------------

Use ``pip`` to install Clime from `PyPI <http://pypi.python.org/>`_.

.. code-block:: bash

    $ sudo pip install clime

Or visit our page for more methods of installation.

CLI-ize ME!
-----------

Here is the usage of Clime.

Clime is designed to easily use, so it is very easy. You have two ways to CLI-ize your program.

In Source Code
""""""""""""""

Add two lines below into your source:

>>> import clime
>>> clime.main()

Recommend to put the codes into the ``if __name__ == '__main__':`` block.

In Shell
""""""""

If you want to convert a moudle temporarily, you can use the ``clime``
command.

.. code-block:: bash

    $ sudo ln -s /usr/local/lib/python<VERSION>/dist-packages/clime.py /usr/bin/clime
    $ sudo chmod 755 /usr/bin/clime 

    $ clime <module_name> <args_for_module>

Examples
""""""""

Here is a simple example of Clime:

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

Use it in shell:

.. code-block:: bash

    $ python singlecmd.py --help
    usage: singlecmd.py [-b] [-l VAL] s 
       or: singlecmd.py onlyme [-b] [-l VAL] s 

    Here is docstring of module.

    $ python singlecmd.py onlyme --help
    usage: singlecmd.py onlyme [-b] [-l VAL] s 

    Here is docstring of function.

    $ python singlecmd.py test -b -loption_arg
    s: test
    b: False
    l: option_arg

    $ python singlecmd.py test -bbb -l one -l two -l three
    s: test
    b: 2
    l: ['one', 'two', 'three']

See the `clime.Command.parse <deeper.html#clime.Command.parse>`_ section for more details
about argument parsing.

You can find more examples under the ``clime/examples`` of source tarball of Clime.

OK, it is the all of the usage of Clime. If you want to know more details or
help Clime, please visit the below page

.. toctree::
   :maxdepth: 1

   deeper

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

