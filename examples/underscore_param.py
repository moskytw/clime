#!/usr/bin/env python
# -*- coding: utf-8 -*-

def echo(first, _second, _third='3rd'):
    '''

    Examples:

    $ py underscore_param.py 1st 2rd --third 3rd
    underscore_param.py: echo() got an unexpected keyword argument 'third'

    $ py underscore_param.py 1st 2rd ---third 3rd
    1st 2rd 3rd

    $ py underscore_param.py 1st 2rd --_third 3rd
    1st 2rd 3rd

    $ py underscore_param.py 1st ---second 2rd --_third 3rd
    1st 2rd 3rd
    '''

    print first, _second, _third

if __name__ == '__main__':
    from clime import now

