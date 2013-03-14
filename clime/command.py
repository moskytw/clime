#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from re import compile
from collections import defaultdict
from inspect  import getdoc, isbuiltin
from .helpers import getargspec, autotype

Empty = type('Empty', (object, ), {
    '__nonzero__': lambda self: False,
    '__repr__'   : lambda self: 'Empty',
})()

class Command(object):
    '''Make a function, a built-in function or a bound method accept
    arguments from command line.

    .. versionchanged:: 0.1.4
       It is almost rewritten.'''

    arg_desc_re = compile(r'^\s*-')

    arg_re = compile(r'--?(?P<key>[^ =,]+)[ =]?(?P<meta>[^ ,]+)?')

    arg_type_map = {
        'n': int, 'num': int, 'number': int,
        's': str, 'str': str, 'string': str,
        None: autotype
    }

    def __init__(self, func):

        self.func = func

        arg_names, vararg_name, keyarg_name, arg_defaults = getargspec(func)

        # copy the argument spec info to instance
        self.arg_names = arg_names
        self.vararg_name = vararg_name
        self.keyarg_name = keyarg_name
        self.arg_defaults = arg_defaults or []

        # additional information
        self.arg_name_set = set(arg_names)
        self.arg_default_map = dict((k, v) for k, v in zip(
            *map(reversed, (self.arg_names, self.arg_defaults))
        ))

        # try to find the metas and aliases out

        self.arg_meta_map = {}
        self.alias_arg_map = {}

        doc = getdoc(func)
        if not doc: return

        for line in doc.splitlines():
            if self.arg_desc_re.match(line):

                aliases_set = set()
                for m in self.arg_re.finditer(line):
                    key, meta = m.group('key', 'meta')
                    self.arg_meta_map[key] = meta
                    aliases_set.add(key)

                arg_name_set = self.arg_name_set & aliases_set
                aliases_set -= arg_name_set

                if arg_name_set:
                    arg_name = arg_name_set.pop()
                    for alias in aliases_set:
                        self.alias_arg_map[alias] = arg_name

    def dealias(self, key):
        return self.alias_arg_map.get(key, key)

    def cast(self, arg_name, val):
        meta = self.arg_meta_map.get(arg_name)
        if meta is not None:
            meta = meta.strip('<>').lower()
        type = self.arg_type_map[meta]
        return type(val)

    def scan(self, raw_args=None):
        '''For backward compatibility.'''
        return self.parse(raw_args)

    def parse(self, raw_args=None):

        if raw_args is None:
            raw_args = sys.argv[1:]
        elif isinstance(raw_args, str):
            raw_args = raw_args.split()

        # collect the arguments from the raw arguments

        pargs = []
        kargs = defaultdict(list)

        while raw_args:

            key = None
            val = Empty
            arg_name = None

            if raw_args[0].startswith('-'):

                # '-m=hello' or '--msg=hello'
                key, _, val = raw_args.pop(0).partition('=')

                if key.startswith('--'):
                    key = key[2:]
                else:
                    # '-nnn'       -> sep=4
                    # '-nnnmhello' -> sep=5
                    sep = 1
                    for c in key[1:]:
                        if c in self.arg_name_set or c in self.alias_arg_map:
                            sep += 1
                        else:
                            break

                    # '-nnn'       -> 'nn'
                    # '-nnnmhello' -> 'nnn'
                    for c in key[1:sep-1]:
                        arg_name = self.dealias(c)
                        kargs[arg_name].append(Empty)

                    if not val:
                        # '-mhello'
                        val = key[sep:] or Empty
                    key = key[sep-1]
                    # '-nnn'       -> key='n', val=Empty
                    # '-nnnmhello' -> key='m', val='hello'

                if not val:
                    # ['-m', 'hello'] or ['--msg', 'hello']
                    if raw_args and not raw_args[0].startswith('-'):
                        val = raw_args.pop(0)
            else:
                val = raw_args.pop(0)

            casted_val = self.cast(key, val)

            if key:
                arg_name = self.dealias(key)
                kargs[arg_name].append(casted_val)
            else:
                pargs.append(casted_val)

        # rearrange the collected kargs
        kargs = dict(kargs)
        for arg_name, collected_vals in kargs.items():
            default = self.arg_default_map.get(arg_name)
            if isinstance(default, bool):
                # swith the boolean value if default is a bool
                kargs[arg_name] = not default
            elif all(val is Empty for val in collected_vals):
                # count the Empty if the all vals are Empty
                kargs[arg_name] = len(collected_vals)
            else:
                # take the last value
                kargs[arg_name] = next(val for val in reversed(collected_vals) if val is not Empty)

        # keyword-first resolving
        for pos, name in enumerate(self.arg_names):
            if name in kargs and pos < len(pargs):
                pargs.insert(pos, kargs.pop(name))

        return (pargs, kargs)

    def execute(self, raw_args=None):
        '''Execute this command with `raw_args`.'''

        pargs, kargs = self.parse(raw_args)
        return self.func(*pargs, **kargs)

    def get_usage(self, is_default=False):
        '''Return the usage of this command.

        Example: ::

            files [--mode VAL] [PATHS]...

        If `is_default` is True, it will render usage without function name.
        '''

        # build the reverse alias map
        alias_arg_rmap = {}
        for alias, arg_name in self.alias_arg_map.items():
            aliases = alias_arg_rmap.setdefault(arg_name, [])
            aliases.append(alias)

        usage = []

        # build the arguments which have default value
        for arg_name in self.arg_names[-len(self.arg_defaults):]:

            pieces = []
            for name in alias_arg_rmap.get(arg_name, [])+[arg_name]:
                is_long_opt = len(name) > 1
                pieces.append('%s%s' % ('-' * (1+is_long_opt), name))
                meta = self.arg_meta_map.get(name)
                if meta:
                    if is_long_opt:
                        pieces[-1] += '='+meta
                    else:
                        pieces[-1] += meta

            usage.append('[%s]' % ' | '.join(pieces))

        if self.keyarg_name:
            usage.append('[--<key>=<value>...]')

        # build the arguments which don't have default value
        usage.extend('<%s>' % name for name in self.arg_names[:-len(self.arg_defaults) or None])

        if self.vararg_name:
            usage.append('[<%s>...]' % self.vararg_name)

        if is_default:
            return '%s' % ' '.join(usage)
        else:
            return '%s %s' % (self.func.__name__, ' '.join(usage))

if __name__ == '__main__':

    import doctest
    doctest.testmod()

    def func(msg, default='default value', flag=False, level=0):
        '''It is just a test function.

        -d <str>, --default <str>
        -f, --flag
        -l, --level
        '''
        return number, message

    cmd = Command(func)
    print cmd.arg_names
    print cmd.arg_name_set
    print cmd.vararg_name
    print cmd.keyarg_name
    print cmd.arg_default_map
    print cmd.arg_meta_map
    print cmd.alias_arg_map
    print cmd.get_usage()
    print cmd.parse(['-dhello,world', '-f', '-lll'])
    print cmd.parse(['--default', 'hello,world', '--flag', '--level=3'])
    print cmd.parse(['--default', 'hello,world', '--level=3', '-flllll'])
    print cmd.parse(['--default', 'hello,world', '-flll'])
    print cmd.parse(['-fllldhello,world'])
    print cmd.parse(['-fllld', 'hello,world'])
    print cmd.parse(['-fllld=hello,world'])
    print cmd.parse(['-fllld=1234'])
