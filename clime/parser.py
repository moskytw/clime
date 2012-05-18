#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .helper import autotype, getargspec, getoptmetas, sepopt, smartreduce

class Parser(object):

    def __init__(self, f):
        args, varargs, keywords, defs = getargspec(f)
        args = args or []
        defs = defs or []

        bindings  = {}
        defvals   = {}
        mflags    = set()
        for arg, val in zip( *map(reversed, (args, defs)) ):
            bindings['%s%s' % ('-' * (1 + (len(arg) > 1)), arg)] = arg
            defvals[arg] = val
            if isinstance(val, bool): mflags.add(arg)

        for optmetas in getoptmetas(f.__doc__ or ''):
            try:
                boundopt = next(opt for opt, meta in optmetas if opt in bindings)
            except StopIteration:
                pass
            else:
                for opt, meta in optmetas:
                    bindings.setdefault(opt, bindings[boundopt])

        self.args     = args
        self.bindings = bindings
        self.defvals  = defvals
        self.mflags   = mflags

        self.reducers = {}
        #self.varargs  = varargs
        #self.keywords = keywords

    def parse(self, rawargs):

        if isinstance(rawargs, str):
            rawargs = rawargs.split()

        kargs = {}
        pargs = []

        key = None
        for piece in sepopt(rawargs):
            if piece.startswith('-'):
                key = piece.lstrip('-')
                key = self.bindings.get(piece, key)
                if key in self.mflags:
                    kargs[key] = kargs.get(key, 0) + 1
            else:
                if key is None:
                    pargs.append(piece)
                else:
                    reducer = self.reducers.get(key, smartreduce)
                    a = kargs.get(key, None)
                    b = autotype(piece)
                    kargs[key] = reducer(a, b)

        for arg in self.mflags:
            if kargs.get(arg, 0) == 1:
                kargs[arg] = not self.defvals[arg]

        return pargs, kargs

