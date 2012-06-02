#!/usr/bin/env python
# -*- coding: utf-8 -*-

from inspect import getdoc
from .helper import getargspec, getoptmetas, autotype, smartadd 

class ScanError(Exception): pass

class Command(object):

    deftype = staticmethod(autotype)
    metatypes = {'N': int, 'NUM': int}

    def __init__(self, func):
        args, vararg, keyword, defvals = getargspec(func)

        # basic infomation
        self.func = func
        self.args = args
        self.vararg = vararg
        self.keyword = keyword

        # 1. put the args and defvals into a dict
        # 2. collect the mode-flags
        self.defaults = {}
        self.mflags = set()
        for arg, defval in zip( *map(reversed, (args, defvals)) ):
            self.defaults[arg] = defval
            if isinstance(defval, bool):
                self.mflags.add(arg)

        # collect the aliases and metavars
        self.bindings = {}
        self.metavars = {}
        doc = getdoc(func)
        if not doc: return 

        args = set(args)
        for optmetas in getoptmetas(doc):
            for opt, meta in optmetas:
                self.metavars[opt] = meta
            opts, metas = zip(*optmetas)
            opts = set(opts)
            target = (opts & args).pop()
            opts -= args
            for opt in opts:
                self.bindings[opt] = target

    def scan(self, rawargs):

        def mktypewrapper(t):
            def typewrpper(o):
                try:
                    return t(o)
                except ValueError:
                    raise ScanError("option '%s' must be %s" % (opt, t.__name__))
            return typewrpper

        def gettype(opt):
            meta = self.metavars.get(opt, None)
            t = self.metatypes.get(meta, self.deftype)
            return mktypewrapper(t)

        def nextarg():
            if rawargs and not rawargs[0].startswith('-'):
                return rawargs.pop(0)
            else:
                raise ScanError("option '%s' needs a value" % opt)

        if isinstance(rawargs, str):
            rawargs = rawargs.split()
        else:
            rawargs = rawargs[:]

        pargs = []
        kargs = {}

        while rawargs:
            piece, _, npiece = rawargs.pop(0).partition('=')
            if npiece: rawargs.insert(0, npiece)

            plen = len(piece)
            if piece.startswith('-'):

                if plen >= 3 and piece[1] == '-':
                    # keyword option: --options [value]
                    opt = piece[2:]
                    key = self.bindings.get(opt, opt)
                    vals = kargs.setdefault(key, [])
                    if key in self.mflags:
                        vals.append( None )
                    else:
                        vals.append( gettype(opt)( nextarg() ) )
                    continue

                if plen >= 2:
                    # letter option: -abco[value] or --abco [value]
                    epiece = enumerate(piece); next(epiece)
                    for i, opt in epiece:
                        key = self.bindings.get(opt, opt)
                        vals = kargs.setdefault(key, [])
                        if key in self.mflags:
                            vals.append( None )
                        else:
                            if i == plen-1:
                                # -abco value
                                val = nextarg()
                            else:
                                # -abcovalue
                                val = piece[i+1:]
                            vals.append( gettype(opt)(val) )
                            break
                    continue

            # if doesnt start with '-' or length of piece is not enough
            pargs.append(piece)

        # reduce the collected values
        for key, vals in kargs.iteritems():
            val = reduce(smartadd, vals, object)
            kargs[key] = val

        # toggle the bool default value
        for mflag in self.mflags:
            if kargs.get(mflag, 0) is None:
                kargs[mflag] = not self.defaults[mflag]

        return pargs, kargs

    def usage(self):

        optargs = self.defaults.keys()
        optargs.sort()

        rbindings = {}
        for opt, target in self.bindings.iteritems():
            shortcuts = rbindings.setdefault(target, [])
            shortcuts.append(opt)

        usage = []

        for optarg in optargs:
            opts = [optarg]
            opts.extend( rbindings[optarg] )
            for i, opt in enumerate(opts):
                opts[i] ='%s%s' % ('-' * (1+(len(opt)>1)), opt)
                meta = self.metavars[opt]
                if meta:
                    opts[i] += ' '+meta
            usage.append('[%s]' % ' | '.join(opts))

        posargs = self.args[:len(optargs)-1]
        usage.extend( map(str.upper, posargs) )
            
        return ' '.join(usage)
