#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from inspect  import getmembers, isclass
from .command import Command, ScanError

class Program(object):

    def __init__(self, obj=None, default=None, name=None):
       self.members = getmembers(obj)
       self.default = default
       self.name = name or sys.argv[0]

    def complain(s):
        print >> sys.stderr, '%s: %s' % (self.name, s)

    def main(rawargs):

        if isinstance(rawargs, str):
            rawargs = rawargs.split()
        else:
            rawargs = rawargs[:]

        cmdname = rawargs[0]
        command = None

        try:
            command = self.members[cmdname]
            rawargs.pop(0)
        except KeyError:
            pass

        if self.default:
            cmdname = self.default
            try:
                command = self.members[cmdname]
            except KeyError:
                pass

        
