from distutils.core import setup
import clime

long_description = open('README.rst').read()

setup(
    name    = 'clime',
    description = 'Easily convert your Python functions into multi-command CLI program.',
    long_description = long_description,
    version = '0.1',
    author  = 'Mosky',
    author_email = 'mosky.tw@gmail.com',
    url = 'http://docs.mosky.tw/clime',
    py_modules = ['clime'],
)

import os
import stat
import glob

climepys = glob.glob('/usr/local/lib/python2.*/dist-packages/clime.py')
climepys.sort()
os.symlink(climepys[-1], '/usr/bin/clime')
os.chmod('/usr/bin/clime', 0o755)
