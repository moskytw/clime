#!/usr/bin/env python
# -*- coding: utf-8 -*-

# file: pyramid.py

def draw(story, squash=1):
    '''It draws a pyramid.

    -s <int>, --squash=<int>
    '''

    ground_len = 1 + (story-1) * squash * 2

    for i in range(1, ground_len+1, squash*2):
        print ('*'*i).center(ground_len)

if __name__ == '__main__':
    import clime.now
