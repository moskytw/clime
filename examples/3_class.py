#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Cmd:
    '''<I am from class>'''

    def donothing(self):
        '''<I am from method>'''
        pass

    def echo(self, string):
        '''Echo what you saied.'''
        print string

if __name__ == '__main__':
    import clime
    clime.main( Cmd() )
