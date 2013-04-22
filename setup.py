from distutils.core import setup

from clime import __version__

setup(
    name    = 'clime',
    description = 'Let you convert any module into a multi-command CLI program without any configuration.',
    long_description = open('README.rst').read(),
    version = __version__,
    author  = 'Mosky',
    author_email = 'mosky.tw@gmail.com',
    url = 'http://clime.mosky.tw/',
    packages = ['clime'],
)
