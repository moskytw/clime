#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from inspect  import getmembers, isclass, isgenerator, getdoc
from .command import Command, ScanError

class Program(object):

    def __init__(self, obj=None, defcmdname=None, progname=None):

        self.cmdfs = {}
        if obj is None:
            obj = sys.modules['__main__']

        if isinstance(obj, dict):
            self.cmdfs = obj
        else:
            for name, obj in getmembers(obj):
                if not callable(obj): continue
                if isclass(obj): continue
                if name.startswith('_'): continue
                self.cmdfs[name] = obj

        self.defcmdname = defcmdname
        if len(self.cmdfs) == 1:
            self.defcmdname = self.cmdfs.keys()[0]
        self.progname = progname or sys.argv[0]

    def main(self, rawargs=None):

        if rawargs is None:
            rawargs = sys.argv[1:]
        elif isinstance(rawargs, str):
            rawargs = rawargs.split()
        else:
            rawargs = rawargs[:]

        cmdname = None
        cmdf = None
        try:
            cmdname = rawargs.pop(0)
        except IndexError:
            pass
        else:
            cmdf = self.cmdfs.get(cmdname, None)

        if cmdf is None and self.defcmdname:
            if cmdname is not None:
                rawargs.insert(0, cmdname)
            cmdf = self.cmdfs.get(self.defcmdname, None)
        
        if cmdf is None:
            self.printusage()
            return

        if '--help' in rawargs:
            self.printusage(cmdf)
            return

        cmd = Command(cmdf)
        obj = cmd(rawargs)
        if obj:
            if isgenerator(obj):
                for result in obj:
                    print result
            else:
                print obj

    def printusage(self, cmdf=None):

        usages = []
        cmd = None

        if cmdf is None:

            if self.defcmdname is not None:
                cmdf = self.cmdfs[self.defcmdname]
                usages.append( Command(cmdf).getusage() )

            for cmdname in sorted(self.cmdfs.keys()):
                if cmdname != self.defcmdname:
                    cmdf = self.cmdfs[cmdname]
                    usages.append( Command(cmdf).getusage() )

        else:
            cmd = Command(cmdf)
            usages.append(cmd.getusage())

        for i, usage in enumerate(usages):
            if i == 0:
                print 'usage:',
            else:
                print '   or:',
            print usage

        if cmd:
            print
            print getdoc(cmd.func)
