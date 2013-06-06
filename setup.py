from setuptools import setup

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
    license = 'MIT',
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    entry_points = {
         'console_scripts': [
             'clime = clime.__main__:main',
        ]
    }
)
