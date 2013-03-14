#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from inspect  import getmembers, ismodule, isbuiltin, isfunction, ismethod, isgenerator, getdoc
from .command import Command, ScanError

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
        Added `white_list`, `black_list`, `doc` and `debug`.

    .. versionchanged:: 0.1.5
        Renamed `defcmd` and `progname`.

    .. versionchanged:: 0.1.4
       It is almost rewritten.
    '''

    def __init__(self, obj=None, default=None, white_list=None, black_list=None, name=None, doc=None, debug=False):

        obj = obj or sys.modules['__main__']
        self.obj = obj

        if hasattr(obj, 'items'):
            obj_items = obj.items()
        else:
            obj_items = getmembers(obj)

        if hasattr(obj, '__all__'):
            white_list = obj.__all__

        tests = (isbuiltin, isfunction, ismethod)

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
        elif raw_args[0] == '--help':
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

        if '--help' in raw_args:
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
            if isgenerator(return_val):
                for return_val in return_val:
                    print result
            else:
                print return_val

    def print_usage(self, cmd_name=None):
        '''Print the usages of all commands or a command.'''

        def append_usage(cmd_name, is_default=False):
            # nonlocal usages
            cmd_func = self.command_funcs[cmd_name]
            usages.append(Command(cmd_func).get_usage(is_default))

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
                append_usage(cmd_name, is_default=True)
            append_usage(cmd_name)

        # print the usages.
        iusages = iter(usages)
        print 'usage:', next(iusages)
        for usage in iusages:
            print '   or:', usage

        # find the doc.
        if cmd_name is None:
            doc = self.doc if self.doc else getdoc(self.obj)
        else:
            doc = getdoc(self.command_funcs[cmd_name])

        # print the doc.
        if doc:
            print
            print doc
