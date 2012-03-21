#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import sys, getopt
import inspect
import textwrap
from types import BuiltinFunctionType

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

    def strbetween(s, a, b):
        return s[s.find(a): s.rfind(b)]

    argspecdoc = func.__doc__.split('\n')[0]
    argpart = strbetween(argspecdoc, '(', ')')
    args = argpart.split(',')
    args = [ arg.strip(' ()[]') for arg in args ]

    defaultpart = strbetween(argspecdoc, '[', ']')
    defaultcount = defaultpart.count(',')

    return (args, None, None, (None,) * defaultcount or None)

class Command(object):
    '''Make a function to accpect arguments from command line.
    
    You can set the aliases is a `dict` which key is the argument name of
    `func`; the value is the alias of this key.
    
    Or you can set aliases as a attribute of the `func`. Example: ::
        
        def cmd(long_option=None): pass
        cmd.aliases = {'s': 'long_option'}

    '''

    def __init__(self, func, aliases=None):
        self.func = func

        if isinstance(func, BuiltinFunctionType):
            spec = getargspecfromdoc(func)
        else:
            spec = inspect.getargspec(func)

        self.argnames = spec[0] or []
        self.varname  = spec[1]
        defvals       = spec[3] or []
        self.defaults = dict( zip(self.argnames[::-1], defvals[::-1]) )

        self.opts = ( aliases or getattr(func, 'aliases', {}) ).copy()
        for name in self.defaults:
            self.opts[ name.replace('_', '-') ] = name
        
    def parse(self, usrargs):
        '''Parse the `usrargs`, and return a tuple (`posargs`, `optargs`).

        `usargs` can be `string` or `list`.

        It uses the *keyword-first resolving* -- If keyword and positional
        arguments are at same place, the keyword argument will take this
        place and push the positional argument to next.
        
        Example:
            
        >>> def files(mode='r', *paths):
        >>>     print mode, paths
        >>> 
        >>> files_cmd = Command(files)
        >>> files_cmd.parse('--mode w f1.txt f2.txt')
        (['w', 'f1.txt', 'f2.txt'], {})
        >>> files_cmd('--mode w f1.txt f2.txt')
        w ('f1.txt', 'f2.txt')    

        If an no-value options is found and the value in default of function is
        boolean, it will put the opposite boolean into `optargs`.

        >>> def test(b=True, x=None):
        >>>     print b, x
        >>> 
        >>> test_cmd = Command(test)
        >>> test_cmd('-b')
        False None

        If duplicate options are found and

        1. the default of function is boolean: it will count this options;
        2. otherwise: it will put the value into a list.

        >>> test_cmd('-bbb -x first -x second -x third')
        3 ['first', 'second', 'third']
        '''

        if isinstance(usrargs, str):
            usrargs = usrargs.split()

        # convert opts into getopt syntax
        shortopts = []
        longopts  = []
        for opt, argname in self.opts.iteritems():
            ismflag = isinstance(self.defaults.get(argname), bool)
            islong  = len(opt) > 1
            (shortopts, longopts)[islong].append( opt + ( '' if ismflag else ':='[islong] ) )

        _optargs, posargs = getopt.gnu_getopt(usrargs, ''.join(shortopts), longopts)

        optargs = {}

        for key, value in _optargs:
            key   = key.lstrip('-')
            value = autotype(value)

            try:
                existvalue = optargs[key]
            except KeyError:
                optargs[key] = value
            else:
                if value == '':
                    if isinstance(existvalue, int):
                        optargs[key] += 1
                    else:
                        optargs[key] = 2
                elif isinstance(existvalue, list):
                    existvalue.append(value)
                else:
                    optargs[key] = [existvalue, value]

        posargs = map(autotype, posargs)

        # de-alias
        for alias, val in optargs.items():
            real = self.opts[alias]
            optargs[real] = val
            if real != alias:
                del optargs[alias]

        # toggle bool in defaults
        for argname, val in self.defaults.iteritems():
            if optargs.get(argname, 'skip') == '' and isinstance(val, bool):
                optargs[argname] = not val
            else:
                optargs.setdefault(argname, val)

        # de-keyword (keyword-first resolving)
        for pos, argname in enumerate(self.argnames):
            palen = len(posargs)
            if pos > palen: break
            try:
                val = optargs[argname]
            except KeyError:
                pass
            else:
                posargs.insert(pos, val)
                del optargs[argname]

        # process for Built-in Function
        # because the Built-in Function only accpect posargs
        if isinstance(self.func, BuiltinFunctionType):
            posargs.extend([None] * (len(self.argnames) - len(posargs)))
            for key, value in optargs.items():
                posargs[self.argnames.index(key)] = value
            optargs = {}
            try:
                posargs = posargs[:-posargs.index(None) or None]
            except ValueError:
                pass

        return posargs, optargs

    def get_usage(self, ignore_cmd=False):
        '''Return the usage of this command.

        Example:

            files [--mode VAL] [paths]...
        '''
        if ignore_cmd:
            usage = '%s ' % sys.argv[0]
        else:
            usage = '%s %s ' % (sys.argv[0], self.func.__name__)
        for alias, real in self.opts.iteritems():
            hyphen = '-' * (1 + (len(alias) > 1))
            val = (' VAL', '')[isinstance(self.defaults.get(real, None), bool)]
            usage += '[%s%s%s] ' % (hyphen, alias, val)
        for argname in self.argnames[:-len(self.defaults) or None]:
            usage += '%s ' % argname
        if self.varname:
            usage += '[%s]... ' % self.varname
        return usage

    def help(self):
        '''Print help to stdout. Conatins usage and the docstring of this
        function.'''

        print 'usage:', self.get_usage()
        doc = getdoc(self.func)
        if doc:
            print
            print doc

    def __call__(self, usrargs):
        '''Parse `usargs` and call the function.'''

        posargs, optargs = self.parse(usrargs)
        return self.func(*posargs, **optargs)

class Program(object):
    '''Convert module into multi-command CLI program.
    
    `default` is the default function when a user calls `Program` object without command.'''

    def __init__(self, module=None, default=None):

        self.default = default
        self.module  = module or sys.modules['__main__']

        self.funcs = {}
        for name, attr in self.module.__dict__.iteritems():
            if not callable(attr):   continue
            if name.startswith('_'): continue
            self.funcs[name] = attr

        if len(self.funcs) == 1 and self.default is None:
            self.default = self.funcs.values()[0]

    def get_cmds_usages(self):
        '''Return a list contains the usage of the functions in this program.'''
        return [ Command(func).get_usage() for func in self.funcs.values() ]

    def get_tip(self, func=None):
        '''Return the 'Try ... for more information.' tip.'''

        if not func:
            target = sys.argv[0]
        else:
            target = '%s %s' % (sys.argv[0], func.__name__)

        return 'Try `%s --help` for more information.' % target

    def help(self):
        '''Print the complete help of this program.'''

        usages = self.get_cmds_usages()
        if self.default:
            usages.insert(0, Command(self.default).get_usage(True))
        for i, usage in enumerate(usages):
            if i == 0:
                print 'usage:',
            else:
                print '   or:',
            print usage                

        doc = getdoc(self.module)
        if doc:
            print
            print doc

    def help_error(self, func=None):
        '''Print the tip.'''

        print self.get_tip(func)

    def __call__(self, usrargs):
        '''Use it as a CLI program.'''
        
        if not usrargs or usrargs[0] == '--help':
            self.help()
            sys.exit(0)

        try:
            func = self.funcs[usrargs[0]]
        except KeyError:
            func = self.default
        else:
            usrargs.pop(0)

        if func is None:
            print '%s: No command \'%s\' found.' % (sys.argv[0], usrargs[0])
            self.help_error()
            sys.exit(2)

        cmd = Command(func)

        try:
            val = cmd(usrargs)
        except (getopt.GetoptError, TypeError), err:

            if hasattr(err, 'opt') and err.opt == 'help':
                cmd.help()
            else:
                print '%s: %s' % (sys.argv[0], str(err))
                self.help_error(func)

            sys.exit(2)
        else:
            if val: print val
            sys.exit(0)


def main(default=None, module=None):
    '''Use it to simply convert your program.
    
    `default` is the default function if call this program without command.

    `module` is the module you want to convert. Default is the '__main__' in
    ``sys.modules``.'''

    prog = Program(module, default)
    prog(sys.argv[1:])

if __name__ == '__main__':

    def clime(module_name, *args):
        '''Dynamicly make a module into CLI program.'''
        module = __import__(module_name)
        prog = Program(module)
        prog(sys.argv[2:])

    fakemodule = lambda: ''
    fakemodule.clime = clime

    main(module=fakemodule)
