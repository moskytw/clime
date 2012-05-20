#!/usr/bin/env python
# -*- coding: utf-8 -*-

from inspect import getdoc
from .helper import getargspec, getoptmetas, autotype

class ArgSpec(object):

    def __init__(self, func):
        args, vararg, keyword, defvals = getargspec(func)

        self.args = args
        self.vararg = vararg
        self.keyword = keyword

        self.defaults = {}
        self.mflags = set()
        for arg, defval in zip( *map(reversed, (args, defvals)) ):
            self.defaults[arg] = defval
            if isinstance(defval, bool):
                self.mflags.add(arg)

        self.bindings = {}
        doc = getdoc(func)
        if not doc: return 

        args = set(args)
        for optmetas in getoptmetas(doc):
            opts, metas = zip(*optmetas)
            opts = set( opt.lstrip('-') for opt in opts )
            target = (opts & args).pop()
            opts -= args
            for opt in opts:
                self.bindings[opt] = target

    def parse(self, rawargs):

        if isinstance(rawargs, str):
            rawargs = rawargs.split()

        pargs = []
        kargs = []

        while rawargs:
            piece = rawargs.pop(0)
            equalsign = piece.find('=')
            if equalsign != -1:
                piece = piece[:equalsign]
                rawargs.insert(0, piece[equalsign+1:])
            plen = len(piece)
            if piece.startswith('-'):
                if plen >= 3 and piece[1] == '-':
                    key = piece[2:]
                    key = self.bindings.get(key, key)
                    vals = kargs.setdefault(key, [])
                    if key not in self.mflags:
                        vals.append( autotype(rawargs.pop(0)) )
                    continue

                if plen >= 2:
                    for i, c in enumerate(piece[1:]):
                        key = self.bindings.get(c, c)
                        if c not in self.mflags:
                            break

                    for c in piece[1:i]:
                        key = self.bindings.get(c, c)
                        vals = kargs.setdefault(key, [])
                        vals.append(None)

                    #TODO
