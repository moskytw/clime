from distutils.core import setup
import clime

setup(
        name    = 'clime',
        description = clime.__doc__[:clime.__doc__.find('\n')],
        long_description = clime.__doc__,
        version = '0.1',
        author  = 'Mosky',
        author_email = 'mosky.tw@gmail.com',
        py_modules = ['clime'],
    )
