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
        'N': int, 'NUM': int, 'NUMBER': int,
        'S': str, 'STR': str, 'STRING': str,
        '<n>': int, '<num>': int, '<number>': int,
        '<s>': str, '<str>': str, '<string>': str,
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

        self.arg_alias_map = {}
        self.arg_meta_map = {}

        for line in doc.splitlines():
            if self.arg_desc_re.match(line):

                meta_map = {}
                aliases_set = set()
                for m in self.arg_re.finditer(line):
                    key, meta = m.group('key', 'meta')
                    aliases_set.add(key)
                    meta_map[key] = meta

                arg_name_set = self.arg_name_set & aliases_set
                aliases_set -= arg_name_set

                if arg_names:
                    arg_name = arg_name_set.pop()
                    self.arg_meta_map[arg_name] = meta_map[arg_name]
                    for alias in aliases_set:
                        self.arg_alias_map[alias] = arg_name

    def cast(self, key, val, meta=None):
        return self.arg_meta_map.get(meta)(val)

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

        If `isdefault` is True, it will render usage without function name.
        '''

        rbindings = {}
        for opt, target in self.bindings.iteritems():
            shortcuts = rbindings.setdefault(target, [])
            shortcuts.append(opt)

        usage = []

        for optarg in optargs:
            opts = [optarg]
            opts.extend( rbindings.get(optarg, []) )
            for i, opt in enumerate(opts):
                opts[i] ='%s%s' % ('-' * (1+(len(opt)>1)), opt.replace('_', '-'))
                meta = self.metavars.get(opt, None)
                if meta:
                    opts[i] += ' '+meta
            usage.append('[%s]' % ' | '.join(opts))

        posargs = self.args[:-len(optargs) or None]
        usage.extend( map(str.upper, posargs) )

        if self.vararg:
            usage.append('[%s]... ' % self.vararg.upper())

        if is_default:
            return '%s' % ' '.join(usage)
        else:
            name = self.func.__name__
            return '%s %s' % (name, ' '.join(usage))

if __name__ == '__main__':

    def f(number, message='default messagea', switcher=False):
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
