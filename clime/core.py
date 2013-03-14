#!/usr/bin/env python
# -*- coding: utf-8 -*-

__all__ = ['Command', 'Program']

import sys
import inspect
import re
from collections import defaultdict
from .util import *

Empty = type('Empty', (object, ), {
    '__nonzero__': lambda self: False,
    '__repr__'   : lambda self: 'Empty',
})()

class Command(object):
    '''Make a function, a built-in function or a bound method accept
    arguments from command line.

    .. versionchanged:: 0.1.4
       It is almost rewritten.'''

    arg_desc_re = re.compile(r'^\s*-')

    arg_re = re.compile(r'--?(?P<key>[^ =,]+)[ =]?(?P<meta>[^ ,]+)?')

    arg_type_map = {
        'n': int, 'num': int, 'number': int,
        'i': int, 'int': int, 'integer': int,
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
        self.arg_defaults = arg_defaults or tuple()

        # additional information
        self.arg_name_set = set(arg_names)
        self.arg_default_map = dict((k, v) for k, v in zip(
            *map(reversed, (self.arg_names, self.arg_defaults))
        ))

        # try to find the metas and aliases out

        self.arg_meta_map = {}
        self.alias_arg_map = {}

        doc = inspect.getdoc(func)
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

    def _dealias(self, key):
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
                        arg_name = self._dealias(c)
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

            if key:
                arg_name = self._dealias(key)
                kargs[arg_name].append(val)
            else:
                pargs.append(val)

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
                val = next(val for val in reversed(collected_vals) if val is not Empty)
                # cast this key arg
                if arg_name in self.arg_meta_map:
                    kargs[arg_name] = self.cast(arg_name, val)
                if self.keyarg_name:
                    kargs[arg_name] = self.cast(self.keyarg_name, val)

        # keyword-first resolving
        isbuiltin = inspect.isbuiltin(self.func)
        for pos, name in enumerate(self.arg_names):
            if name in kargs and (pos < len(pargs) or isbuiltin):
                pargs.insert(pos, kargs.pop(name))

        # cast the pos args
        for i, parg in enumerate(pargs):
            if i < len(self.arg_names):
                pargs[i] = self.cast(self.arg_names[i], parg)
            elif self.vararg_name:
                pargs[i] = self.cast(self.vararg_name, parg)

        return (pargs, kargs)

    def execute(self, raw_args=None):
        '''Execute this command with `raw_args`.'''

        pargs, kargs = self.parse(raw_args)
        return self.func(*pargs, **kargs)

    def get_usage(self, without_name=False):
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

        if without_name:
            return '%s' % ' '.join(usage)
        else:
            return '%s %s' % (self.func.__name__, ' '.join(usage))

class Program(object):
    '''Convert a module or dict into a multi-command CLI program.

    :param obj: The `object` you want to convert.
    :type obj: a module or a mapping
    :param default: The default command name.
    :type default: str
    :param white_list: The white list of the commands. By default, it uses the attribute, ``__all__``, of a module.
    :type white_list: list
    :param black_list: The black list of the commands.
    :type black_list: list
    :param name: The name of this program. It is used to show the error messages.
    :type name: str
    :param doc: The documentation on module level.
    :type doc: str
    :param debug: It prints the full traceback if True.
    :type name: bool

    .. versionadded:: 0.1.5
        Added `white_list`, `black_list`, `ignore_help`, `doc` and `debug`.

    .. versionchanged:: 0.1.5
        Renamed `defcmd` and `progname`.

    .. versionchanged:: 0.1.4
       It is almost rewritten.
    '''

    def __init__(self, obj=None, default=None, white_list=None, black_list=None, ignore_help=False, name=None, doc=None, debug=False):

        obj = obj or sys.modules['__main__']
        self.obj = obj

        if hasattr(obj, 'items'):
            obj_items = obj.items()
        else:
            obj_items = inspect.getmembers(obj)

        if hasattr(obj, '__all__'):
            white_list = obj.__all__

        tests = (inspect.isbuiltin, inspect.isfunction, inspect.ismethod)

        self.command_funcs = {}
        for name, obj in obj_items:
            if name.startswith('_'): continue
            if not any(test(obj) for test in tests): continue
            if white_list is not None and name not in white_list: continue
            if black_list is not None and name in black_list: continue
            self.command_funcs[name] = obj

        self.default = default
        if len(self.command_funcs) == 1:
            self.default = self.command_funcs.keys()[0]

        self.ignore_help = ignore_help
        self.name = name or sys.argv[0]
        self.doc = doc
        self.debug = debug

    def complain(self, msg):
        '''Print an error message `msg` with the name of this program to stderr.'''
        print >> sys.stderr, '%s: %s' % (self.name, msg)

    def main(self, raw_args=None):
        '''Start to parse the arguments from CLI and send them to a command.

        :param raw_args: The arguments from command line. By default, it takes from ``sys.argv``.
        :type raw_args: list
        '''

        if raw_args is None:
            raw_args = sys.argv[1:]
        elif isinstance(raw_args, str):
            raw_args = raw_args.split()

        # try to find the command name in the raw arguments.
        cmd_name = None
        cmd_func = None

        if len(raw_args) == 0:
            pass
        elif not self.ignore_help and raw_args[0] == '--help':
            self.print_usage()
            return
        else:
            cmd_func = self.command_funcs.get(raw_args[0])
            if cmd_func is not None:
                cmd_name = raw_args.pop(0)

        if cmd_func is None:
            # we can't find the command name in normal procedure
            if self.default:
                cmd_name = cmd_name
                cmd_func = self.command_funcs[self.default]
            else:
                self.print_usage()
                return

        if not self.ignore_help and '--help' in raw_args:
            # the user requires help of this command.
            self.print_usage(cmd_name)
            return

        # convert the function to Command object.
        cmd = Command(cmd_func)

        try:
            # execute the command with the raw arguments.
            return_val = cmd.execute(raw_args)
        except Exception, e:
            if self.debug:
                from traceback import print_exception
                print_exception(*sys.exc_info())
                return
            else:
                self.complain(e)
                return

        if return_val is not None:
            if inspect.isgenerator(return_val):
                for return_val in return_val:
                    print result
            else:
                print return_val

    def print_usage(self, cmd_name=None):
        '''Print the usages of all commands or a command.'''

        def append_usage(cmd_name, without_name=False):
            # nonlocal usages
            cmd_func = self.command_funcs[cmd_name]
            usages.append(Command(cmd_func).get_usage(without_name))

        usages = []
        cmd_func = None

        if cmd_name is None:
            # prepare all usages.
            if self.default is not None:
                append_usage(self.default, True)
            for name in sorted(self.command_funcs.keys()):
                append_usage(name)
        else:
            # prepare the usage of a command.
            if self.default == cmd_name:
                append_usage(cmd_name, without_name=True)
            append_usage(cmd_name)

        # print the usages.
        iusages = iter(usages)
        print 'usage:', next(iusages)
        for usage in iusages:
            print '   or:', usage

        # find the doc.
        if cmd_name is None:
            doc = self.doc if self.doc else inspect.getdoc(self.obj)
        else:
            doc = inspect.getdoc(self.command_funcs[cmd_name])

        # print the doc.
        if doc:
            print
            print doc

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
