#!/usr/bin/env python
# -*- coding: utf-8 -*-

# file: pyramid.py

from __future__ import print_function

import sys

def draw(story, squash=1, verbose=False):
    '''It draws a pyramid.

    -s <int>, --squash=<int>  make fat pyramid
    -v, --verbose             show the args from `squash` and `--squash`
    '''

    if verbose:
        print('Story : {}'.format(story), file=sys.stderr)
        print('Squash: {}'.format(squash), file=sys.stderr)
        print(file=sys.stderr)

    ground_len = 1 + (story-1) * squash * 2

    for i in range(1, ground_len+1, squash*2):
        print(('*'*i).center(ground_len))

if __name__ == '__main__':
    import clime.now
