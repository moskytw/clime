#!/usr/bin/env python
# -*- coding: utf-8 -*-

# file: pyramid.py

import sys

def draw(story, squash=1, verbose=False):
    '''It draws a pyramid.

    -s <int>, --squash=<int>  make fat pyramid
    -v, --verbose             show the args from `squash` and `--squash`
    '''

    if verbose:
        print >> sys.stderr, 'Story : {}'.format(story)
        print >> sys.stderr, 'Squash: {}'.format(squash)
        print >> sys.stderr

    ground_len = 1 + (story-1) * squash * 2

    for i in range(1, ground_len+1, squash*2):
        print ('*'*i).center(ground_len)

if __name__ == '__main__':
    import clime.now
