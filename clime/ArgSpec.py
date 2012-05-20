#!/usr/bin/env python
# -*- coding: utf-8 -*-

from inspect import getdoc
from .helper import getargspec, getoptmetas, autotype, smartreducer

class ParseError(Exception): pass

class ArgSpec(object):

    deftype = staticmethod(autotype)
    metatypes = {'N': int, 'NUM': int}

    def __init__(self, func):
        args, vararg, keyword, defvals = getargspec(func)

        self.func = func
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
        self.metavars = {}
        doc = getdoc(func)
        if not doc: return 

        args = set(args)
        for optmetas in getoptmetas(doc):
            for opt, meta in optmetas:
                self.metavars[opt.lstrip('-')] = meta
            opts, metas = zip(*optmetas)
            opts = set( opt.lstrip('-') for opt in opts )
            target = (opts & args).pop()
            opts -= args
            for opt in opts:
                self.bindings[opt] = target

    def parse(self, rawargs):

        def sepequal(piece):
            equalsign = piece.find('=')
            npiece = ''
            if equalsign != -1:
                npiece = piece[equalsign+1:]
                piece = piece[:equalsign]
            return piece, npiece

        def mktypewrapper(t):
            def typewrpper(o):
                try:
                    return t(o)
                except ValueError:
                    raise ParseError("option '%s' must be %s" % (opt, t.__name__))
            return typewrpper

        def gettype(opt):
            meta = self.metavars.get(opt, None)
            t = self.metatypes.get(meta, self.deftype)
            return mktypewrapper(t)

        def nextarg():
            if rawargs and not rawargs[0].startswith('-'):
                return rawargs.pop(0)
            else:
                raise ParseError("option '%s' need a value" % opt)

        if isinstance(rawargs, str):
            rawargs = rawargs.split()

        pargs = []
        kargs = {}

        while rawargs:
            piece, npiece = sepequal( rawargs.pop(0) )
            if npiece: rawargs.insert(0, npiece)

            plen = len(piece)
            if piece.startswith('-'):

                if plen >= 3 and piece[1] == '-':
                    # keyword option
                    opt = piece[2:]
                    key = self.bindings.get(opt, opt)
                    vals = kargs.setdefault(key, [])
                    if key in self.mflags:
                        vals.append( None )
                    else:
                        vals.append( gettype(opt)( nextarg() ) )
                    continue

                if plen >= 2:
                    # letter option
                    epiece = enumerate(piece); next(epiece)
                    for i, opt in epiece:
                        key = self.bindings.get(opt, opt)
                        vals = kargs.setdefault(key, [])
                        if key in self.mflags:
                            vals.append( None )
                        else:
                            if i == plen-1:
                                val = nextarg() 
                            else:
                                val = piece[i+1:]
                            vals.append( gettype(opt)(val) )
                            break
                    continue

            # if doesnt start with '-' or length of piece is not enough
            pargs.append(piece)

        for key, vals in kargs.iteritems():
            val = reduce(smartreducer, vals, object)
            kargs[key] = val

        for mflag in self.mflags:
            if kargs.get(mflag, 0) is None:
                kargs[mflag] = not self.defaults[mflag]

        return pargs, kargs
