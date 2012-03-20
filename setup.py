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
