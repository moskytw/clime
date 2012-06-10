#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, re, inspect

def autotype(s):
    '''Automative detect the type (int, float or string) of `s` and convert `s`
    into it.'''

    if not isinstance(s, str):
        return s

    if s.isdigit():
        return int(s)

    try:
        return float(s)
    except ValueError:
        return s

def getargspec(func):
    '''Get the argument specification of the `func`.
    
    The `func` is a Python function, built-in function or bound method.
    
    It get the argument specification by parsing documentation of the
    function if `func` is a built-in function.
    
    .. versionchanged:: 0.1.4
       Remove `self` automatively if `func` is a method.

    .. versionadded:: 0.1.3
    '''

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
    args = ( arg.strip(' ()[]') for arg in args )
    args = [ arg for arg in args if arg ]

    defaultpart = strbetween(argspecdoc, '[', ']')
    defaultcount = len([d for d in defaultpart.split(',') if d.strip('[]')])

    return (args or None, None, None, (None,) * defaultcount or None)

DOCOPTDESC_RE = re.compile(r' *(-.+?) {2,}')

DOCOPT_RE = re.compile(

        r'''--?({0}) # option
           (?:
              \[?
              [= ]
              ({0})  # metavar
           )?
           ,?
        ''' \
       .format('[^\s,=\[\]]+')

   , re.X)

def getoptmetas(doc):
    '''Yield the option and the metavar in each line.
    
    In each iteration, it will yield a list like: ::
        
        [('opt1', 'META'), ('opt2', None), ...]

    .. versionadded:: 0.1.4
    '''

    for line in doc.split('\n'):
        m = DOCOPTDESC_RE.match(line)
        if m is None: continue
        yield [m.groups() for m in DOCOPT_RE.finditer(m.group(1))]

def smartlyadd(a, b):
    '''Smartly add `a` and `b`.
    
    +------------+--------+----------------+
    | a          | b      | return         |
    +============+========+================+
    | object     | <any>  | b              |
    +------------+--------+----------------+
    | None       | None   | 2              |
    +------------+--------+----------------+
    | None       | <else> | b              |
    +------------+--------+----------------+
    | int        | None   | a+1            |
    +------------+--------+----------------+
    | appendable | <any>  | a.append(b); a |
    +------------+--------+----------------+
    | <else>     | <any>  | [a, b]         |
    +------------+--------+----------------+
    
    The `object` which is class ``object`` repersents the hyper None.

    .. versionadded:: 0.1.4
    '''

    if a is object:
        return b
    elif a is None:
        if b is None:
            return 2
        else:
            return b
    elif isinstance(a, int) and b is None:
        return a+1
    elif hasattr(a, 'append'):
        a.append(b)
        return a
    else:
        return [a, b]

def ensureargs(args=None):
    '''Ensure the args is a list.
    
    return sys.argv if args is None'''

    if args is None:
        return sys.argv
    elif isinstance(args, str):
        return args.split()
    elif isinstance(args, list):
        return args
    elif hasattr(args, '__iter__'):
        return list(args)
    else:
        return None
