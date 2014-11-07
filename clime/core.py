#!/usr/bin/env python
# -*- coding: utf-8 -*-

__all__ = ['start', 'customize', 'CMD_SUFFIX', 'Program', 'Command']

import sys
import inspect
import re
from os.path import basename
from collections import defaultdict
from .util import json, autotype, getargspec

Empty = type('Empty', (object, ), {
    '__nonzero__': lambda self: False,
    '__repr__'   : lambda self: 'Empty',
})()

class Command(object):
    '''Make a Python function or a built-in function accepts arguments from
    command line.

    :param func: a function you want to convert
    :type func: Python function or built-in function
    :param name: the name of this command
    :type name: str

    .. versionchanged:: 0.1.5
        It is rewritten again. The API is same as the previous version, but some
        behaviors may be different. Please read :py:meth:`Command.parse` for
        more details.

    .. versionchanged:: 0.1.4
        It is almost rewritten.
    '''

    arg_desc_re = re.compile(r'^\s*-')
    '''It is used to filter argument descriptions in a docstring.

    The regex is ``r'^\s*-'`` by default. It means any line starts with a hyphen
    (-), and whitespace characters before this hyphen are ignored.
    '''

    arg_re = re.compile(r'-(?P<long>-)?(?P<key>(?(long)[^ =,]+|.))[ =]?(?P<meta>[^ ,]+)?')
    '''After it gets descriptions by :py:attr:`Command.arg_desc_re` from a
    docstring, it extracts an argument name (or alias) and a metavar from each
    description by this regex.

    The regex is
    ``-(?P<long>-)?(?P<key>(?(long)[^ =,]+|.))[ =]?(?P<meta>[^ ,]+)?``
    by default. The following formats will be parsed correctly:

    - ``--key meta``
    - ``--key=meta``
    - ``-k meta``
    - ``-k=meta``
    - ``-kmeta``
    '''

    arg_type_map = {
        'n': int, 'num': int, 'number': int,
        'i': int, 'int': int, 'integer': int,
        's': str, 'str': str, 'string': str,
        'f': float, 'float': float,
        'json': json,
        None: autotype
    }
    '''A metavar implies a type.

    The ``n``, ``num``, ``number``, ``i``, ``int`` and ``integer`` mean a `int`.
    The ``s``, ``str`` and ``string`` mean a `str`.
    The ``f`` and ``float`` mean a `float`.

    It also supports to use ``json``. It converts a json from user to a Python
    type.

    If you don't set a metavar, it will try to guess a correct type.

    The metavars here are normalized. Metavars from docstrings will be
    normalized, too. For example, ``JSON`` and ``<json>`` are equal to ``json``.
    '''

    def __init__(self, func, name=None):

        self.name = name
        self.func = func

        arg_names, vararg_name, keyarg_name, arg_defaults = getargspec(func)

        # copy the argument spec info to instance
        self.arg_names = arg_names
        self.vararg_name = vararg_name
        self.keyarg_name = keyarg_name
        self.arg_defaults = arg_defaults or tuple()

        # additional information
        self.no_defult_args_len = len(self.arg_names) - len(self.arg_defaults)
        self.arg_name_set = set(arg_names)
        self.arg_default_map = dict(zip(
            *map(reversed, (self.arg_names, self.arg_defaults))
        ))

        # try to find metas and aliases out

        self.arg_meta_map = {}
        self.alias_arg_map = {}

        doc = inspect.getdoc(func)
        if not doc: return

        for line in doc.splitlines():

            if not self.arg_desc_re.match(line): continue

            arg_part, _, desc_part = line.strip().partition('  ')

            aliases_set = set()
            for m in self.arg_re.finditer(arg_part):
                key, meta = m.group('key', 'meta')
                key = key.replace('-', '_')
                self.arg_meta_map[key] = meta
                aliases_set.add(key)

            arg_name_set = self.arg_name_set & aliases_set
            if not arg_name_set: continue

            aliases_set -= arg_name_set
            arg_name = arg_name_set.pop()
            for alias in aliases_set:
                self.alias_arg_map[alias] = arg_name

    def dealias(self, alias):
        '''It maps `alias` to an argument name. If this `alias` maps noting, it
        return `alias` itself.

        :param key: an alias
        :type key: str
        :rtype: str
        '''
        return self.alias_arg_map.get(alias, alias)

    def cast(self, arg_name, val):
        '''Cast `val` by `arg_name`.

        :param arg_name: an argument name
        :type arg_name: str
        :param val: a value
        :type val: any
        :rtype: any
        '''
        meta = self.arg_meta_map.get(arg_name)
        if meta is not None:
            meta = meta.strip('<>').lower()
        type = self.arg_type_map[meta]
        return type(val)

    def parse(self, raw_args=None):
        """Parse the raw arguments.

        :param raw_args: raw arguments
        :type raw_args: a list or a str
        :rtype: double-tuple: (pargs, kargs)

        .. versionadded:: 0.1.5

        Here are examples:

        >>> def repeat(message, times=2, count=False):
        ...     '''It repeats the message.
        ...
        ...     -m=<str>, --message=<str>  The description of this option.
        ...     -t=<int>, --times=<int>
        ...     -c, --count
        ...     '''
        ...     s = message * times
        ...     return len(s) if count else s
        ...
        >>> repeat('string', 3)
        'stringstringstring'

        Make a :class:`~clime.core.Command` instance:

        >>> repeat_cmd = Command(repeat)
        >>> repeat_cmd.build_usage()
        'repeat [-t <int> | --times=<int>] [-c | --count] <message>'
        >>> repeat_cmd.execute('Hi!')
        'Hi!Hi!'

        You can also use options (keyword arguments) to assign arguments
        (positional arguments):

        >>> repeat_cmd.execute('--message=Hi!')
        'Hi!Hi!'
        >>> repeat_cmd.execute('--message Hi!')
        'Hi!Hi!'

        The short version defined in docstring:

        >>> repeat_cmd.execute('-mHi!')
        'Hi!Hi!'
        >>> repeat_cmd.execute('-m=Hi!')
        'Hi!Hi!'
        >>> repeat_cmd.execute('-m Hi!')
        'Hi!Hi!'

        It counts how many times options appear, if you don't specify a value:

        >>> repeat_cmd.execute('--times=4 Hi!')
        'Hi!Hi!Hi!Hi!'
        >>> repeat_cmd.execute('Hi! -tttt')
        'Hi!Hi!Hi!Hi!'
        >>> repeat_cmd.execute('-ttttm Hi!')
        'Hi!Hi!Hi!Hi!'

        However, if a default value is a boolean, it just switches the boolean
        value and does it only one time.

        Mix them all:

        >>> repeat_cmd.execute('-tttt --count Hi!')
        12
        >>> repeat_cmd.execute('-ttttc Hi!')
        12
        >>> repeat_cmd.execute('-ttttcc Hi!')
        12
        >>> repeat_cmd.execute('-ttccttm Hi!')
        12

        It is also supported to collect arbitrary arguments:

        >>> def everything(*args, **kargs):
        ...     return args, kargs

        >>> everything_cmd = Command(everything)
        >>> everything_cmd.build_usage()
        'everything [--<key>=<value>...] [<args>...]'

        >>> everything_cmd.execute('1 2 3')
        ((1, 2, 3), {})

        >>> everything_cmd.execute('--x=1 --y=2 --z=3')
        ((), {'y': 2, 'x': 1, 'z': 3})
        """

        if raw_args is None:
            raw_args = sys.argv[1:]
        elif isinstance(raw_args, str):
            raw_args = raw_args.split()

        # collect arguments from the raw arguments

        pargs = []
        kargs = defaultdict(list)

        # consume raw_args
        while raw_args:

            # try to find `arg_name` and `val`
            arg_name = None
            val = Empty

            # '-a...', '--arg...', but no '-'
            if raw_args[0].startswith('-') and len(raw_args[0]) >= 2:

                # partition by eq sign
                # -m=hello
                # --message=hello -> val='hello'
                # --message=      -> val=''
                # --bool          -> val=Empty
                before_eq_str, eq_str, val = raw_args.pop(0).partition('=')
                if not eq_str:
                    val = Empty

                if before_eq_str.startswith('--'):
                    arg_name = self.dealias(before_eq_str[2:].replace('-', '_'))
                else:

                    # if it starts with only '-', it may be various

                    # find the start index (sep) of val
                    # '-nnn'       -> sep=4 (the length of this str)
                    # '-nnnmhello' -> sep=5 (the char 'h')
                    sep = 1
                    for c in before_eq_str[1:]:
                        if c in self.arg_name_set or c in self.alias_arg_map:
                            sep += 1
                        else:
                            break

                    # handle the bool option sequence
                    # '-nnn'       -> 'nn'
                    # '-nnnmhello' -> 'nnn'
                    for c in before_eq_str[1:sep-1]:
                        arg_name = self.dealias(c)
                        kargs[arg_name].append(Empty)

                    # handle the last option
                    # '-nnn'       -> 'n' (the 3rd n)
                    # '-nnnmhello' -> 'm'
                    arg_name = self.dealias(before_eq_str[sep-1])

                    if val is Empty:
                        val = before_eq_str[sep:] or Empty

                # handle if the val is next raw_args
                # --message hello
                # --bool hello (note the hello shall be a pargs)
                # -nnnm hello
                # -nnnb hello
                if (
                    # didn't get val
                    val is Empty and
                    # this arg_name need a explicit val
                    not isinstance(self.arg_default_map.get(arg_name), bool) and
                    # we have thing to take
                    raw_args and not raw_args[0].startswith('-')
                ):
                    val = raw_args.pop(0)
            else:
                val = raw_args.pop(0)

            if arg_name:
                kargs[arg_name].append(val)
            else:
                pargs.append(val)

        # compact the collected kargs
        kargs = dict(kargs)
        for arg_name, collected_vals in kargs.items():
            default = self.arg_default_map.get(arg_name)
            if isinstance(default, bool):
                # switch the boolean value if default is a bool
                kargs[arg_name] = not default
            elif all(val is Empty for val in collected_vals):
                if isinstance(default, int):
                    kargs[arg_name] = len(collected_vals)
                else:
                    kargs[arg_name] = None
            else:
                # take the last value
                val = next(val for val in reversed(collected_vals) if val is not Empty)
                # cast this key arg
                if not self.keyarg_name or arg_name in self.arg_meta_map:
                    kargs[arg_name] = self.cast(arg_name, val)
                else:
                    kargs[arg_name] = self.cast(self.keyarg_name, val)

        # add the defaults to kargs
        for arg_name, default in self.arg_default_map.items():
            if arg_name not in kargs:
                kargs[arg_name] = default

        # keyword-first resolving
        isbuiltin = inspect.isbuiltin(self.func)
        for pos, name in enumerate(self.arg_names):
            if name in kargs and (pos < len(pargs) or isbuiltin):
                pargs.insert(pos, kargs.pop(name))

        # cast the pos args
        for i, parg in enumerate(pargs):
            if i < self.no_defult_args_len:
                pargs[i] = self.cast(self.arg_names[i], parg)
            elif self.vararg_name:
                pargs[i] = self.cast(self.vararg_name, parg)

        return (pargs, kargs)

    scan = parse
    '''
    .. deprecated:: 0.1.5
        Use :py:meth:`Command.parse` instead.
    '''

    def execute(self, raw_args=None):
        '''Execute this command with `raw_args`.

        :param raw_args: raw arguments
        :type raw_args: a list or a str
        :rtype: any
        '''

        pargs, kargs = self.parse(raw_args)
        return self.func(*pargs, **kargs)

    def build_usage(self, without_name=False):
        '''Build the usage of this command.

        :param without_name: Make it return an usage without the function name.
        :type without_name: bool
        :rtype: str
        '''

        # build reverse alias map
        alias_arg_rmap = {}
        for alias, arg_name in self.alias_arg_map.items():
            aliases = alias_arg_rmap.setdefault(arg_name, [])
            aliases.append(alias)

        usage = []

        # build the arguments which have default value
        if self.arg_defaults:
            for arg_name in self.arg_names[-len(self.arg_defaults):]:

                pieces = []
                for name in alias_arg_rmap.get(arg_name, [])+[arg_name]:

                    is_long_opt = len(name) > 1
                    pieces.append('%s%s' % ('-' * (1+is_long_opt), name.replace('_', '-')))

                    meta = self.arg_meta_map.get(name)
                    if meta is None:
                        # autometa
                        default = self.arg_default_map[self.dealias(name)]
                        if isinstance(default, bool):
                            continue
                        elif default is None:
                            meta = '<value>'
                        else:
                            meta = '<default:{!r}>'.format(default)

                    if is_long_opt:
                        pieces[-1] += '='+meta
                    else:
                        pieces[-1] += ' '+meta

                usage.append('[%s]' % ' | '.join(pieces))

        if self.keyarg_name:
            usage.append('[--<key>=<value>...]')

        # build the arguments which don't have default value
        usage.extend('<%s>' % name.replace('_', '-') for name in self.arg_names[:-len(self.arg_defaults) or None])

        if self.vararg_name:
            usage.append('[<%s>...]' % self.vararg_name.replace('_', '-'))

        if without_name:
            return '%s' % ' '.join(usage)
        else:
            return '%s %s' % ((self.name or self.func.__name__).replace('_', '-'), ' '.join(usage))

    get_usage = build_usage
    '''
    .. deprecated:: 0.2.5
        Use :py:meth:`Command.build_usage` instead.
    '''


CMD_SUFFIX = re.compile('^(?P<name>.*?)_cmd$')
'''
It matches the function whose name ends with ``_cmd``.

The regex is ``^(?P<name>.*?)_cmd$``.

Usually, it is used with :py:func:`start`:

::

    import clime
    clime.start(white_pattern=clime.CMD_SUFFIX)
'''

class Program(object):
    '''Convert a module or mapping into a multi-command CLI program.

    .. seealso::
        There is a shortcut of using :py:class:`Program` --- :py:func:`start`.

    :param obj: an `object` you want to convert
    :type obj: a module or a mapping

    :param default: the default command name
    :type default: str

    :param white_list: the white list of commands; By default, it uses the attribute, ``__all__``, of a module.
    :type white_list: list

    :param white_pattern: the white pattern of commands; The regex should have a group named ``name``.
    :type white_pattern: RegexObject

    :param black_list: the black list of commands
    :type black_list: list

    :param ignore_help: Let it treat ``--help`` or ``-h`` as a normal argument.
    :type ignore_help: bool

    :param ignore_return: Make it prevent printing the return value.
    :type ignore_return: bool

    :param name: the name of this program; It is used to show error messages. By default, it takes the first arguments from CLI.
    :type name: str

    :param doc: the documentation for this program
    :type doc: str

    :param debug: It prints a full traceback if it is True.
    :type name: bool

    .. versionchanged:: 0.3
        The ``-h`` option also trigger help text now.

    .. versionadded:: 0.1.9
        Added `white_pattern`.

    .. versionadded:: 0.1.6
        Added `ignore_return`.

    .. versionadded:: 0.1.5
        Added `white_list`, `black_list`, `ignore_help`, `doc` and `debug`.

    .. versionchanged:: 0.1.5
        Renamed `defcmd` and `progname`.

    .. versionchanged:: 0.1.4
       It is almost rewritten.
    '''

    def __init__(self, obj=None, default=None, white_list=None, white_pattern=None, black_list=None, ignore_help=False, ignore_return=False, name=None, doc=None, debug=False):

        obj = obj or sys.modules['__main__']
        self.obj = obj

        if hasattr(obj, 'items'):
            obj_items = obj.items()
        else:
            obj_items = inspect.getmembers(obj)

        if not white_list and hasattr(obj, '__all__'):
            white_list = obj.__all__

        tests = (inspect.isbuiltin, inspect.isfunction, inspect.ismethod)

        self.command_funcs = {}
        for obj_name, obj in obj_items:

            if obj_name.startswith('_'): continue
            if not any(test(obj) for test in tests): continue
            if white_list is not None and obj_name not in white_list: continue
            if black_list is not None and obj_name in black_list: continue

            if white_pattern:
                match = white_pattern.match(obj_name)
                if not match: continue
                obj_name = match.group('name')

            self.command_funcs[obj_name] = obj

        self.default = default
        if len(self.command_funcs) == 1:
            self.default = self.command_funcs.keys()[0]

        self.ignore_help = ignore_help
        self.ignore_return = ignore_return
        self.name = name or basename(sys.argv[0])
        self.doc = doc
        self.debug = debug

    def complain(self, msg):
        '''Print `msg` with the name of this program to `stderr`.'''
        print >> sys.stderr, '%s: %s' % (self.name, msg)

    def main(self, raw_args=None):
        '''Start to parse the raw arguments and send them to a
        :py:class:`~clime.core.Command` instance.

        :param raw_args: The arguments from command line. By default, it takes from ``sys.argv``.
        :type raw_args: list
        '''

        if raw_args is None:
            raw_args = sys.argv[1:]
        elif isinstance(raw_args, str):
            raw_args = raw_args.split()

        # try to find a command name in the raw arguments.
        cmd_name = None
        cmd_func = None

        if len(raw_args) == 0:
            pass
        elif not self.ignore_help and raw_args[0] in ('--help', '-h'):
            self.print_usage()
            return
        else:
            cmd_func = self.command_funcs.get(raw_args[0].replace('-', '_'))
            if cmd_func is not None:
                cmd_name = raw_args.pop(0).replace('-', '_')

        if cmd_func is None:
            # we can't find a command name in normal procedure
            if self.default:
                cmd_name = cmd_name
                cmd_func = self.command_funcs[self.default]
            else:
                self.print_usage()
                return

        if not self.ignore_help and '--help' in raw_args:
            # the user requires help of this command
            self.print_usage(cmd_name)
            return

        # convert the function to a Command object
        cmd = Command(cmd_func, cmd_name)

        try:
            # execute the command with the raw arguments
            return_val = cmd.execute(raw_args)
        except BaseException, e:
            if self.debug:
                from traceback import print_exception
                print_exception(*sys.exc_info())
            else:
                self.complain(e)
            sys.exit(1)

        if not self.ignore_return and return_val is not None:
            if inspect.isgenerator(return_val):
                for i in return_val:
                    print i
            else:
                print return_val

    def print_usage(self, cmd_name=None):
        '''Print the usage(s) of all commands or a command.'''

        def append_usage(cmd_name, without_name=False):
            # nonlocal usages
            cmd_func = self.command_funcs[cmd_name]
            usages.append(Command(cmd_func, cmd_name).build_usage(without_name))

        usages = []
        cmd_func = None

        if cmd_name is None:
            # prepare all usages
            if self.default is not None:
                append_usage(self.default, True)
            for name in sorted(self.command_funcs.keys()):
                append_usage(name)
        else:
            # prepare the usage of a command
            if self.default == cmd_name:
                append_usage(cmd_name, without_name=True)
            append_usage(cmd_name)

        # print the usages
        iusages = iter(usages)
        print 'usage:', next(iusages)
        for usage in iusages:
            print '   or:', usage

        # find the doc

        # find the module-level doc
        if cmd_name is None:
            if self.doc:
                doc = self.doc
            elif inspect.ismodule(self.obj):
                doc = inspect.getdoc(self.obj)
            else:
                doc = None

            # fallback to default command if still not found
            if not doc:
                cmd_name = self.default

        if cmd_name:
            doc = inspect.getdoc(self.command_funcs[cmd_name])

        # print the doc
        if doc:
            print
            print doc
            print

def start(*args, **kargs):
    '''It is same as ``Program(*args, **kargs).main()``.

    .. versionchanged:: 1.0
        renamed from `customize` to `start`

    .. versionadded:: 0.1.6

    .. seealso::
        :py:class:`Program` has the detail of arguments.
    '''

    prog = Program(*args, **kargs)
    prog.main()

    return prog

# for backward compatibility
customize = start
'''
.. deprecated:: 0.1.6
    Use :py:func:`start` instead.
'''

if __name__ == '__main__':

    import doctest
    doctest.testmod()

    def read_json(json=None):
        '''
        options:
            --json=<json>
        '''
        return json

    read_json_cmd = Command(read_json)

    print '---'
    print read_json_cmd.build_usage()
    print read_json_cmd.execute('[1,2,3]')
    print read_json_cmd.execute(['--json', '{"x": 1}'])
    print '---'

    prog = Program(white_list=['read_json'], debug=True)
    prog.main()
    # python -m clime.core read-json --help
    # python -m clime.core read-json '{"x": 1}'
    # python -m clime.core read-json --json='{"x":1}'
