#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from re import compile
from inspect  import getdoc, isbuiltin
from .helpers import getargspec, getoptmetas, autotype, smartlyadd

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
        self.mode_flags = set(arg_name for arg_name in self.arg_names if self.is_flag(arg_name))

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

        self.mode_flags.union(alias for alias in self.alias_arg_map if self.is_flag(self.dealias(alias)))

    def dealias(self, key):
        return self.alias_arg_map.get(key, key)

    def is_flag(self, arg_name):
        arg_default = self.arg_default_map.get(arg_name)
        return isinstance(arg_default, bool)

    def cast(self, arg_name, val):
        meta = self.arg_meta_map.get(arg_name)
        if meta is not None:
            meta = meta.strip('<>').lower()
        type = self.arg_type_map[None]
        return type(val)

    def merge(self, arg_name, val, new_val):
        return smartlyadd(val, new_val)

    def scan(self, raw_args=None):
        '''Scan the `raw_args`, and return a tuple (`pargs`, `kargs`).

        `raw_args` can be `string` or `list`.

        Uses *keyword-first resolving* -- If keyword and positional arguments
        are at same place, the keyword argument takes this place and pushes
        the positional argument to next one.

        Example:

        >>> def files(mode='r', *paths):
        ...     print mode, paths
        ...
        >>> files_cmd = Command(files)
        >>> files_cmd.scan('--mode w f1.txt f2.txt')
        (['w', 'f1.txt', 'f2.txt'], {})
        >>> files_cmd.execute('--mode w f1.txt f2.txt')
        w ('f1.txt', 'f2.txt')

        If an no-value options is given a function in which a default value is boolean type, it will put the opposite boolean into `optargs`.

        If no option is given to a function in which a default value is boolean type, it will put the opposite boolean value into `optargs`.

        >>> def test(b=False, x=None):
        ...     print b, x
        ...
        >>> test_cmd = Command(test)
        >>> test_cmd.execute('-b')
        True None

        On the other hand, if more than one options are given to a function and

        1. the default of function is boolean: it will count this options;
        2. otherwise: it will put the value into a list.

        >>> test_cmd.execute('-bbb -x first -x second -x third')
        3 ['first', 'second', 'third']

        .. versionchanged:: 0.1.4
           Use custom parser instead of `getopt`.

        .. versionchanged:: 0.1.4
           It is rewritten from `Command.parse` (0.1.3).

        '''

        if raw_args is None:
            raw_args = sys.argv[1:]
        elif isinstance(raw_args, str):
            raw_args = raw_args.split()

        # parse the raw arguments

        pargs = []
        kargs = {}

        while raw_args:

            key = None
            val = None
            arg_name = None

            if raw_args[0].startswith('-'):

                key, _, val = raw_args.pop(0).partition('=')
                if key.startswith('--'):
                    key = key[2:]
                else:
                    for i, c in enumerate(key[1:]):
                        arg_name = self.dealias(c)
                        if self.is_flag(arg_name):
                            if arg_name in kargs:
                                kargs[arg_name] += 1
                            else:
                                kargs[arg_name] = not self.arg_default_map.get(arg_name)
                        else:
                            break
                    else:
                        continue

                    if not val:
                        val = key[i+2:]
                    key = key[i+1]

                arg_name = self.dealias(key)

                if not val:
                    if raw_args and not raw_args[0].startswith('-'):
                        val = raw_args.pop(0)
                    else:
                        val = True
            else:
                val = raw_args.pop(0)

            val = self.cast(key, val)

            if key:
                if arg_name in kargs:
                    kargs[arg_name] = self.merge(arg_name, kargs[arg_name], val)
                else:
                    kargs[arg_name] = val
            else:
                pargs.append(val)

        # keyword-first resolving
        for pos, name in enumerate(self.arg_names):
            if name in kargs and pos < len(pargs):
                pargs.insert(pos, kargs.pop(name))

        return (pargs, kargs)

    def execute(self, raw_args=None):
        '''Execute this command with `raw_args`.'''

        pargs, kargs = self.scan(raw_args)
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

    def f(number=1, b=False, message='default msg', switcher=False, *args, **kargs):
        '''It is just a test function.

        -n=<n>, --number=<n>       The number.
        -m=<str>, --message=<str>  The default.
        -s, --switcher             The switcher.
        '''
        return number, message

    cmd = Command(f)
    print cmd.arg_names
    print cmd.arg_name_set
    print cmd.vararg_name
    print cmd.keyarg_name
    print cmd.arg_default_map
    print cmd.arg_meta_map
    print cmd.alias_arg_map
    print cmd.mode_flags
    print cmd.get_usage()
    print cmd.scan(['--number', '123', '-n', '1', '-bbn', '1'])
