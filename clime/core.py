#!/usr/bin/env python
# -*- coding: utf-8 -*-

__all__ = ['start', 'customize', 'CMD_SUFFIX', 'Program', 'Command']

import sys
import inspect
import re
from os.path import basename
from collections import defaultdict
from .util import *

Empty = type('Empty', (object, ), {
    '__nonzero__': lambda self: False,
    '__repr__'   : lambda self: 'Empty',
})()

class Command(object):
    '''Make a Python function or a built-in function accepts the arguments from
    command line.

    :param func: A function you want to convert to a `command`.
    :type func: a Python function or built-in function
    :param name: the name of this function
    :type name: str

    .. versionchanged:: 0.1.5
        It had been rewritten. The API is same as the previous version, but some
        behaviors may be different. Please read :py:meth:`Command.parse` for
        more details.

    .. versionchanged:: 0.1.4
        It is almost rewritten.
    '''

    arg_desc_re = re.compile(r'^\s*-')
    '''It is used to filter the argument descriptions in a docstring.

    It is ``r'^\s*-'`` by default. It means any line starts with a dash (-), and
    the whitespace characters before this dash are ignored.
    '''

    arg_re = re.compile(r'-(?P<long>-)?(?P<key>(?(long)[^ =,]+|.))[ =]?(?P<meta>[^ ,]+)?')
    '''After it gets the descriptions by :py:attr:`Command.arg_desc_re` from a
    docstring, it extracts the argument name (or alias) and the metavar from
    each description by this regex.

    It is ``-(?P<long>-)?(?P<key>(?(long)[^ =,]+|.))[ =]?(?P<meta>[^ ,]+)?`` by
    default. The following formats will be parsed correctly:

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
        'json': json,
        None: autotype
    }
    '''A metavar implies a type.

    The ``n``, ``num``, ``number``, ``i``, ``int`` and ``integer`` mean a `int`.
    The ``s``, ``str`` and ``string`` mean a `str`.

    It also supports to use ``json``. It converts the json from user to a Python
    type.

    If you don't set a metavar, it will try to guess the correct type.

    The metavars here are normalized. The metavars user defined are also
    normalized before send to here. The ``JSON`` or ``<json>`` are equal to
    ``json``.
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
                    key = key.replace('-', '_')
                    self.arg_meta_map[key] = meta
                    aliases_set.add(key)

                arg_name_set = self.arg_name_set & aliases_set
                aliases_set -= arg_name_set

                if arg_name_set:
                    arg_name = arg_name_set.pop()
                    for alias in aliases_set:
                        self.alias_arg_map[alias] = arg_name

    def dealias(self, alias):
        '''It maps the `alias` to an argument name. If this `alias` maps noting, it
        return the `alias` itself.

        :param key: An alias.
        :type key: str
        :rtype: str
        '''
        return self.alias_arg_map.get(alias, alias)

    def cast(self, arg_name, val):
        '''Convert the `val` from a str to a comportable type.

        It gets the type function by `arg_name`. It maps the `arg_name` to a
        metavar and normalize the metavar to get the type function.

        :param arg_name: The argument name.
        :type arg_name: str
        :param val: The value which got from CLI.
        :type val: any
        :rtype: any
        '''
        meta = self.arg_meta_map.get(arg_name)
        if meta is not None:
            meta = meta.strip('<>').lower()
        type = self.arg_type_map[meta]
        return type(val)

    def scan(self, raw_args=None):
        '''.. deprecated:: 0.1.5
            Use :py:meth:`Command.parse` instead.
        '''
        return self.parse(raw_args)

    def parse(self, raw_args=None):
        """Parse the raw arguments from CLI.

        :param raw_args: The raw arguments from CLI.
        :type raw_args: a list or a str
        :rtype: (pargs, kargs)

        .. versionadded:: 0.1.5

        Here is an example:

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

        >>> repeat_cmd = Command(repeat)

        >>> repeat_cmd.get_usage()
        'repeat [-t<int> | --times=<int>] [-c | --count] <message>'

        >>> repeat_cmd.execute('Hi!')
        'Hi!Hi!'

        >>> repeat_cmd.execute('Hi! 4')
        'Hi!Hi!Hi!Hi!'

        It just maps the CLI arguments to a function call of Python, so they also work well.

        >>> repeat_cmd.execute('--message=Hi!')
        'Hi!Hi!'
        >>> repeat_cmd.execute('--message Hi!')
        'Hi!Hi!'

        >>> repeat_cmd.execute('-mHi!')
        'Hi!Hi!'
        >>> repeat_cmd.execute('-m=Hi!')
        'Hi!Hi!'
        >>> repeat_cmd.execute('-m Hi!')
        'Hi!Hi!'

        It is supported to use '=' or ' ' as the separator for both short or
        long options.

        >>> repeat_cmd.execute('Hi! --times=4')
        'Hi!Hi!Hi!Hi!'
        >>> repeat_cmd.execute('Hi! -tttt')
        'Hi!Hi!Hi!Hi!'

        It uses `keyword-first` resolving which is different from the default
        behavior in Python. Here is an example:

        >>> repeat_cmd.execute('4 --message=Hi!')
        'Hi!Hi!Hi!Hi!'

        >>> repeat(4, message='Hi!')
        Traceback (most recent call last):
            ...
        TypeError: repeat() got multiple values for keyword argument 'message'

        It counts the amount of options, if you don't specify a value.

        >>> repeat_cmd.execute('-m Hi! -tttt --count')
        12
        >>> repeat_cmd.execute('-m Hi! -ttctt')
        12
        >>> repeat_cmd.execute('-ttcttmHi!')
        12
        >>> repeat_cmd.execute('-ttccttmHi!')
        12

        However, if a default value is a boolen, it just switchs the boolean
        value and only does it one time.

        It is also supported to collect arbitrary arguments:

        >>> def everything(*args, **kargs):
        ...     return args, kargs

        >>> everything_cmd = Command(everything)
        >>> everything_cmd.get_usage()
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
                    key = key[2:].replace('-', '_')
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

            if key:
                arg_name = self.dealias(key)
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
                if not self.keyarg_name or arg_name in self.arg_meta_map:
                    kargs[arg_name] = self.cast(arg_name, val)
                else:
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
        '''Execute this command with `raw_args`.

        :param raw_args: The raw arguments from CLI.
        :type raw_args: a list or a str
        :rtype: any
        '''

        pargs, kargs = self.parse(raw_args)
        return self.func(*pargs, **kargs)

    def get_usage(self, without_name=False):
        '''Return the usage of this command.

        :param without_name: Make it return an usage without the function name.
        :type without_name: bool
        :rtype: str
        '''

        # build the reverse alias map
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
                    if meta:
                        if is_long_opt:
                            pieces[-1] += '='+meta
                        else:
                            pieces[-1] += meta

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

CMD_SUFFIX = re.compile('^(?P<name>.*?)_cmd$')
'''
It matchs the function whose name ends with ``_cmd``.

>>> from clime import Program, CMD_SUFFIX
>>> p = Program(white_pattern=CMD_SUFFIX)

The regex is ``^(?P<name>.*?)_cmd$``.
'''

class Program(object):
    '''Convert a module or dict into a multi-command CLI program.

    There is a shortcut of using :py:class:`Program` --- :py:func:`customize`.

    :param obj: The `object` you want to convert.
    :type obj: a module or a mapping

    :param default: The default command name.
    :type default: str

    :param white_list: The white list of the commands. By default, it uses the attribute, ``__all__``, of a module.
    :type white_list: list

    :param white_pattern: The white pattern of commands. The regex should have a group named ``name``.
    :type white_pattern: RegexObject

    :param black_list: The black list of the commands.
    :type black_list: list

    :param ignore_help: Let it treat ``--help`` as a normal argument.
    :type ignore_help: bool

    :param ignore_return: Make it prevent printing the return value.
    :type ignore_return: bool

    :param name: The name of this program. It is used to show the error messages. By default, it takes the first arguments from CLI.
    :type name: str

    :param doc: The documentation on module level.
    :type doc: str

    :param debug: It prints the full traceback if it is True.
    :type name: bool

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
        '''Print an error message `msg` with the name of this program to stderr.'''
        print >> sys.stderr, '%s: %s' % (self.name, msg)

    def main(self, raw_args=None):
        '''Start to parse the arguments from CLI and send them to a
        :py:class:`~clime.core.Command` instance.

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
            cmd_func = self.command_funcs.get(raw_args[0].replace('-', '_'))
            if cmd_func is not None:
                cmd_name = raw_args.pop(0).replace('-', '_')

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
        cmd = Command(cmd_func, cmd_name)

        try:
            # execute the command with the raw arguments.
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
        '''Print the usages of all commands or a command.'''

        def append_usage(cmd_name, without_name=False):
            # nonlocal usages
            cmd_func = self.command_funcs[cmd_name]
            usages.append(Command(cmd_func, cmd_name).get_usage(without_name))

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
            if not doc:
                cmd_name = self.default

        if cmd_name:
            doc = inspect.getdoc(self.command_funcs[cmd_name])

        # print the doc.
        if doc:
            print
            print doc
            print

def start(*args, **kargs):
    '''It is same as the ``Program(*args, **kargs).main()``.

    .. versionchanged:: 1.0
        renamed from `customize` to `start`

    .. versionadded:: 0.1.6

    .. seealso::
        The documentation of the class, :py:class:`Program`, describes the detail of the arguments.
    '''

    prog = Program(*args, **kargs)
    prog.main()

    return prog

# for backward compatibility
customize = start

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
    print read_json_cmd.get_usage()
    print read_json_cmd.execute('[1,2,3]')
    print read_json_cmd.execute(['--json', '{"x": 1}'])
    print '---'

    prog = Program(white_list=['read_json'], debug=True)
    prog.main()
    # python -m clime.core read-json --help
    # python -m clime.core read-json '{"x": 1}'
    # python -m clime.core read-json --json='{"x":1}'
