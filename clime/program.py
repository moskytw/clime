#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from inspect  import getmembers, ismodule, isbuiltin, isfunction, ismethod, isgenerator, getdoc
from .command import Command, ScanError

class Program(object):
    '''Convert a module, class or dict into multi-command CLI program.

    The `obj` is a module, class or dict.

    The `defcmdname` is the default command name.

    The `progname` is the program name while printing error (:meth:`.complain`).

    .. versionchanged:: 0.1.4
       It is almost rewritten.
    '''

    def __init__(self, obj=None, defcmdname=None, progname=None):

        if obj is None:
            obj = sys.modules['__main__']

        if isinstance(obj, dict):
            obj = obj.iteritems()
        else:
            obj = getmembers(obj)

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
        '''Print `s` to `stderr` with the program name prefix'''
        print >> sys.stderr, '%s: %s' % (self.progname, s)

    def main(self, rawargs=None):
        '''The main process of CLI program.

        The `rawargs` is the arguments from command line.

        If `rawargs` is None, it will take `sys.argv[1:]`.'''

        if rawargs is None:
            rawargs = sys.argv[1:]
        elif isinstance(rawargs, str):
            rawargs = rawargs.split()
        else:
            rawargs = rawargs[:]

        # decide the command name
        cmdname = None
        cmdf = None
        try:
            cmdname = rawargs.pop(0)
        except IndexError:
            pass
        else:
            # user requires the global help
            if cmdname == '--help':
                self.printusage()
                return
            cmdf = self.cmdfs.get(cmdname, None)
        
        # use default command name
        if cmdf is None and self.defcmdname:
            if cmdname is not None:
                rawargs.insert(0, cmdname)
            cmdf = self.cmdfs.get(self.defcmdname, None)
        
        # print usage if still got nothing
        if cmdf is None:
            self.printusage()
            return

        # user requires the help of this command
        if '--help' in rawargs:
            self.printusage(cmdname)
            return

        cmd = Command(cmdf)

        try:
            obj = cmd.execute(rawargs)
        except (TypeError, ScanError), e:
            self.complain(e)
            return

        if obj is not None:
            if isgenerator(obj):
                for result in obj:
                    print result
            else:
                print obj

    def printusage(self, cmdname=None):
        '''Print usage of all commands or partial command.'''

        def appendusage(cmdname, isdefault=False):
            cmdf = self.cmdfs[cmdname]
            usages.append( Command(cmdf).getusage(isdefault) )
            return cmdf

        usages = []
        cmdf = None

        if cmdname is None:
            # print all usages

            if self.defcmdname is not None:
                appendusage(self.defcmdname, True)

            for cmdname in sorted(self.cmdfs.keys()):
                appendusage(cmdname)

        else:
            # print partial usage

            if self.defcmdname == cmdname:
                appendusage(cmdname, isdefault=True)
            cmdf = appendusage(cmdname)

        for i, usage in enumerate(usages):
            if i == 0:
                print 'usage:',
            else:
                print '   or:',
            print usage

        doc = getdoc(cmdf)
        if cmdf is not None and doc:
            print
            print doc
