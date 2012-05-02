#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import textwrap
import inspect

def getdoc(obj):
    r'''Get the documentation of `obj`.
    
    And the documentation will be

    1. de-indented; and
    2. added newline char (\\n) at the end.
    '''
    text = inspect.getdoc(obj)
    if text is None: return None

    text += '\n'

    sep = text.index('\n')
    return text[:sep] + textwrap.dedent(text[sep:])

def autotype(s):
    '''Automative detect the type of `s` and convert `s` into it.'''

    if not isinstance(s, str):
        return s

    if s.isdigit():
        return int(s)

    try:
        return float(s)
    except ValueError:
        return s

def getargspecfromdoc(func):
    '''
    .. deprecated:: 0.1.3
       Use :func:`getargspec` instead.

    *Removed.*
    '''

def getargspec(func):
    '''Get the argument specification of the `func`.
    
    `func` is a Python function, built-in function or bound method.
    
    It get the argument specification by parsing documentation of the
    function if `func` is a built-in function.
    
    .. versionchanged:: 0.1.4
       Remove `self` automatively if `func` is a method.

    .. versionadded:: 0.1.3'''

    if inspect.isfunction(func):
        return inspect.getargspec(func)

    if inspect.ismethod(func):
        argspec = inspect.getargspec(func)
        argspec[0].pop(0)
        return argspec

    def strbetween(s, a, b):
        return s[s.find(a): s.rfind(b)]

    argspecdoc = (inspect.getdoc(func) or '').split('\n')[0]
    argpart = strbetween(argspecdoc, '(', ')')
    args = argpart.split(',')
    args = [ arg.strip(' ()[]') for arg in args ]
    args = [ arg for arg in args if arg ]

    defaultpart = strbetween(argspecdoc, '[', ']')
    defaultcount = len([d for d in defaultpart.split(',') if d.strip('[]')])

    return (args or None, None, None, (None,) * defaultcount or None)

DOCOPTDESC_RE = re.compile(r' {2,}(-.+?) {2,}')

DOCOPT_RE = re.compile(

        r'''(--?{0}) # option
           (?:
              \[?
              [= ]
              ({0})  # metaval
           )?
           ,?
        ''' \
       .format('[^\s,=\[\]]+')

   , re.X)

def getoptmetas(doc):

    for line in doc.split('\n'):
        m = DOCOPTDESC_RE.match(line)
        if m is None: continue

        yield [m.groups() for m in DOCOPT_RE.finditer(m.group(1))]

def sepopt(rawargs, mflags=None):

    if mflags is None: mflags = set()

    for piece in rawargs:

        # piece is an optional argument
        if piece.startswith('-'):

            # case: -o=.* | --option=.*
            equalsign = piece.find('=')
            if equalsign != -1:
                yield piece[:equalsign]
                yield piece[equalsign+1:]
                continue

            # case: -o.+
            if piece[1] != '-':
                for i, p in enumerate(piece[1:]):
                    if p in mflags:
                        yield '-%s' % p
                    else:
                        yield '-%s' % p
                        break
                yield piece[i+1:]
                continue

        yield piece

def parse(rawargs, mapping=None, modeflags=None):

    if isinstance(rawargs, str):
        rawargs = rawargs.split()

    if mapping   is None: mapping = {}
    if modeflags is None: modeflags = set()

    kargs = {}
    pargs = []

    collected = None
    for piece in sepopt(rawargs):
        if piece.startswith('-'):
            real = mapping.get(piece, piece.lstrip('-'))
            collected = kargs.setdefault(real, [])
            if piece in modeflags:
                collected.append(1)
                collected = None
        else:
            if collected is not None:
                collected.append(piece)
                collected = None
            else:
                pargs.append(piece)

    return pargs, kargs

def smartreduce(a, b):
    if a is None:
        return b
    elif hasattr(a, 'append'):
        a.append(b)
        return a
    else:
        return [a, b]
