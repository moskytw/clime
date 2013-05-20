#!/usr/bin/env python
# -*- coding: utf-8 -*-

def say(word, name=None):
    if name:
        print '%s, %s!' % (word, name)
    else:
        print '%s!' % word

def hi_cmd(name=None):
    say('Hi', name)

def hello_cmd(name=None):
    say('Hello', name)

if __name__ == '__main__':
    import clime
    clime.start(white_pattern=clime.CMD_SUFFIX)
