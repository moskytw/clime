#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Test results of giving the value to options.'''

def cmd(s, b=True, l=None):
    '''This function will be the default command, because it is the only
    function in this module.
    
    `s` will be a positional option (argument)
    `b` is a mode-flag.
    
    1. Toggle the default value if '-b' appears once.
    2. Count the times of appearing if it appear more times.

    If an option appers more than once, and with values, the values will be
    collect into a list.

    You can use `l` to try this feature.

    See below link to get complete paring infomation:
    http://docs.mosky.tw/clime/deeper.html#clime.Command.parse

    '''

    print 's:', s
    print 'b:', b
    print 'l:', l

if __name__ == '__main__':
    import clime
    clime.main()
