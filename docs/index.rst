.. Clime documentation master file, created by
   sphinx-quickstart on Mon Mar 19 21:47:40 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Introduction
============

Clime lets you convert any module into a multi-command CLI program with zero
configuration.

The main features:

1. It works well with zero configuration. Free you from the configuration hell.
2. Docstring (i.e., help text) is just configuration. When you finish your
   docstring, the configuration of aliases and metavars is also finished.
3. It generates usage for each command automatically.

It is a better choice than the heavy `optparse` or `argparse` for most of CLI
tasks.

.. raw:: html

    <div id="fb-root"></div>
    <script>(function(d, s, id) {
      var js, fjs = d.getElementsByTagName(s)[0];
      if (d.getElementById(id)) return;
      js = d.createElement(s); js.id = id;
      js.src = "//connect.facebook.net/zh_TW/all.js#xfbml=1";
      fjs.parentNode.insertBefore(js, fjs);
    }(document, 'script', 'facebook-jssdk'));</script>


    <style>
    #social-btns div {
        float: left;
    }
    #social-btns:after {
        content: ".";
        display: block;
        font-size: 0;
        clear: both;
    }
    </style>

    <div id='social-btns'>
        <div>
            <iframe src="http://ghbtns.com/github-btn.html?user=moskytw&repo=clime&type=watch&count=true" allowtransparency="true" frameborder="0" scrolling="0" width="85" height="20"></iframe>
        </div>

        <div>
            <div class="fb-like" data-href="http://clime.mosky.tw" data-send="true" data-layout="button_count" data-width="400" data-show-faces="true"></div>
        </div>
    </div>

CLI-ize ME!
-----------

Let me show you Clime with an example.

We have a simple script with a docstring here: ::

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

After we add this line: ::

    import clime.now

.. seealso::
    :mod:`clime.now` describes more about how to customize your program.

Our CLI program is ready!

.. code-block:: bash

    $ python repeat.py twice
    twicetwice

    $ python repeat.py --times=3 thrice
    thricethricethrice

It also generates a pretty usage for this script:

.. code-block:: bash

    $ python repeat.py --help
    usage: [-t <int> | --times=<int>] [-c | --count] <message>
       or: repeat [- t<int> | --times=<int>] [-c | --count] <message>

If you have a docstring in your function, it also shows up in usage manual with
``--help``.

.. code-block:: bash

    $ python repeat.py repeat --help
    usage: [-t <int> | --times=<int>] [-c | --count] <message>
       or: repeat [-t <int> | --times=<int>] [-c | --count] <message>

    It repeats the message.

    options:
        -m=<str>, --message=<str>  The message.
        -t=<int>, --times=<int>
        -c, --count

You can find more examples in the `clime/examples`_.

.. seealso::
    :class:`.Command` describes more about how it works.

.. _`clime/examples`:
    https://github.com/moskytw/clime/tree/master/examples

Installation
------------

Clime is hosted on two different platforms, PyPI_ and GitHub_.

Install from PyPI
~~~~~~~~~~~~~~~~~

Install Clime from PyPI_ for a stable version:

.. code-block:: bash

    $ sudo pip install clime

If you don't have pip, execute

.. code-block:: bash

     $ sudo apt-get install python-pip

to install pip on Debian-base Linux distribution.

Get Clime from GitHub
~~~~~~~~~~~~~~~~~~~~~

If you want to follow the latest version of Clime, use

.. code-block:: bash

    $ git clone git://github.com/moskytw/clime.git

to clone a Clime repository, or download manually from GitHub_.

.. _GitHub:
    http://github.com/moskytw/clime

.. _PyPI:
    http://pypi.python.org/pypi/clime

Take a Deeper Look
------------------

If you want to know more about Clime, here are the details:

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
