#!/usr/bin/env python
# -*- coding: utf-8 -*-

from re import compile
from inspect  import getdoc, isbuiltin
from .helpers import getargspec, getoptmetas, autotype, smartlyadd

class ScanError(Exception): pass

class Command(object):
    '''Make a function, a built-in function or a bound method accept
    arguments from command line.

    .. versionchanged:: 0.1.4
       It is almost rewritten.'''

    arg_desc_re = compile(r'^-')
    arg_re = compile(r'--?(?P<key>[^ =,]+)[ =]?(?P<meta>[^ ,]+)?')
    arg_meta_map = {
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
        self.arg_defaults = arg_defaults

        # additional information
        self.arg_name_set = set(arg_names)
        self.arg_default_map = dict((k, v) for k, v in zip(
            *map(reversed, (arg_names or [], arg_defaults or []))
        ))

        # try to find the metas and aliases out

        doc = getdoc(func)
        if not doc: return

        self.arg_meta_map = {}
        self.arg_alias_map = {}

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
                        self.arg_alias_map[alias] = arg_name

    def get_type(self, meta):
        return self.arg_meta_map.get(meta.strip('<>').lower())

    def cast(self, key, val, meta=None):
        return self.get_type(meta)(val)

    def merge(self, key, val, new_val):
        return smartlyadd(val, new_val)

    def scan(self, raw_args):
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

        >>> def test(b=True, x=None):
        ...     print b, x
        ...
        >>> test_cmd = Command(test)
        >>> test_cmd.execute('-b')
        False None

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

        pass

    def execute(self, raw_args):
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
        arg_alias_rmap = {}
        for alias, arg_name in self.arg_alias_map.items():
            aliases = arg_alias_rmap.setdefault(arg_name, [])
            aliases.append(alias)

        usage = []

        # build the arguments which have default value
        for arg_name in self.arg_names[-len(self.arg_defaults):]:

            pieces = []
            for name in arg_alias_rmap.get(arg_name)+[arg_name]:
                pieces.append('%s%s' % ('-' * (1+(len(name)>1)), name))
                meta = self.arg_meta_map[name]
                if meta:
                    pieces[-1] += ' '+meta

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

    def f(number, message='default messagea', switcher=False, *args, **kargs):
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
    print cmd.arg_alias_map
    print cmd.get_usage()
