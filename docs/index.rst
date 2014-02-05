.. Clime documentation master file, created by
   sphinx-quickstart on Mon Mar 19 21:47:40 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Introduction
============

.. image:: https://travis-ci.org/moskytw/clime.png
   :target: https://travis-ci.org/moskytw/clime

.. image:: https://pypip.in/v/clime/badge.png
   :target: https://pypi.python.org/pypi/clime

.. image:: https://pypip.in/d/clime/badge.png
   :target: https://pypi.python.org/pypi/clime

Clime lets you convert any module into a multi-command CLI program without any
configuration.

Here is a slide which introduces you to Clime:

.. raw:: html

    <iframe src="http://www.slideshare.net/slideshow/embed_code/17237148" width="400" height="337" frameborder="0" marginwidth="0" marginheight="0" scrolling="no" style="border:1px solid #CCC;border-width:1px 1px 0;margin-bottom:5px" allowfullscreen webkitallowfullscreen mozallowfullscreen> </iframe> <div style="margin-bottom:5px"> <strong> <a href="http://www.slideshare.net/moskytw/clime" title="Introduction to Clime" target="_blank">Introduction to Clime</a> </strong> from <strong><a href="http://www.slideshare.net/moskytw" target="_blank">Mosky Liu</a></strong> </div>

The main features:

1. It works well with zero configuration. Free you from the configuration hell.
2. Docstrings (i.e., help texts) is just configurations. When you finish a
   docstring, a configuration of aliases and metavars are also finished.
3. It generates usages for each command automatically.

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

.. seealso::
    :mod:`clime.now` describes more about how to customize your program.

Your CLI program is ready!

.. code-block:: bash

    $ python repeat.py twice
    twicetwice

    $ python repeat.py --times=3 thrice
    thricethricethrice

It also generates a pretty usage for this script:

.. code-block:: bash

    $ python repeat.py --help
    usage: [-t<int> | --times=<int>] [-c | --count] <message>
       or: repeat [-t<int> | --times=<int>] [-c | --count] <message>

If you have a docstring in your function, it also shows up in usage manual with
``--help``.

.. code-block:: bash

    $ python repeat.py repeat --help
    usage: [-t<int> | --times=<int>] [-c | --count] <message>
       or: repeat [-t<int> | --times=<int>] [-c | --count] <message>

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
