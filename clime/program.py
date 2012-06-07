#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from inspect  import getmembers, ismodule, isbuiltin, isfunction, ismethod, isgenerator, getdoc
from .command import Command, ScanError

class Program(object):

    def __init__(self, obj=None, defcmdname=None, progname=None):


        if obj is None:
            obj = sys.modules['__main__']

        if ismodule(obj):
            obj = getmembers(obj)
        elif isinstance(obj, dict):
            obj = obj.iteritems()

        self.cmdfs = {}
        iskinds = (isbuiltin, isfunction, ismethod)
        for name, obj in obj:
            if name.startswith('_'): continue
            if not any( iskind(obj) for iskind in iskinds ): continue
            self.cmdfs[name] = obj

        self.defcmdname = defcmdname
        if len(self.cmdfs) == 1:
            self.defcmdname = self.cmdfs.keys()[0]
        self.progname = progname or sys.argv[0]

    def complain(self, s):
        print >> sys.stderr, '%s: %s' % (self.progname, s)

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

        try:
            obj = cmd(rawargs)
        except (TypeError, ScanError), e:
            self.complain(e)
            return

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
