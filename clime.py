#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import sys, getopt
import inspect
import textwrap

__version__ = '0.1.3'

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
    '''
    .. deprecated:: 0.1.3
       Use :func:`getargspec` instead.

    *Removed.*
    '''

def getargspec(func):
    '''Get the argument specification of the `func`.
    
    `func` is a Python function, built-in function or bound method.
    
    It get the argument specification by parsing documentation of the
    function if `func` is a built-in function.
    
    .. versionadded:: 0.1.3'''

    if inspect.isfunction(func) or inspect.ismethod(func):
        return inspect.getargspec(func)

    def strbetween(s, a, b):
        return s[s.find(a): s.rfind(b)]

    argspecdoc = (inspect.getdoc(func) or '').split('\n')[0]
    argpart = strbetween(argspecdoc, '(', ')')
    args = argpart.split(',')
    args = [ arg.strip(' ()[]') for arg in args ]
    args = [ arg for arg in args if arg ]

    defaultpart = strbetween(argspecdoc, '[', ']')
    defaultcount = len([d for d in defaultpart.split(',') if d.strip('[]')])

    return (args or None, None, None, (None,) * defaultcount or None)

class Command(object):
    '''Make a function, a built-in function or a bound method to accpect
    arguments from command line.
    
    You can set the aliases in a `dict` in ``{alias: real}`` format.
    
    Or you can set aliases as a attribute of the `func`. Example: ::
        
        def cmd(long_option=None): pass
        cmd.aliases = {'s': 'long_option'}

    .. versionadded:: 0.1.3
       Arguments, `name` and `doc`.
    '''

    def __init__(self, func, aliases=None, name=None, doc=None):

        ul2hp = lambda s: s.replace('_', '-')

        self.func = func
        self.name = name or ul2hp( func.__name__ )
        self.doc  = getdoc(func)

        spec = getargspec(func)

        self.argnames = spec[0] or []
        self.varname  = spec[1]
        defvals       = spec[3] or []
        self.defaults = dict( zip(self.argnames[::-1], defvals[::-1]) )

        if inspect.ismethod(func):
            self.argnames.pop(0)

        self.opts = ( aliases or getattr(func, 'aliases', {}) ).copy()
        for name in self.defaults:
            self.opts[ ul2hp( name ) ] = name
        
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

        .. versionadded:: 0.1.1 
            Support the type of `built-in function`
            (``types.BuiltinFunctionType``).

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

        # map all of the optargs to posargs for `built-in function`,
        # because the `built-in function` only accpects posargs
        if inspect.isbuiltin(self.func):
            posargs.extend([None] * (len(self.argnames) - len(posargs)))
            for key, value in optargs.items():
                posargs[self.argnames.index(key)] = value
            optargs = {}
            try:
                posargs = posargs[:-posargs.index(None) or None]
            except ValueError:
                pass

        return posargs, optargs

    def get_usage(self, isdefault=False):
        '''Return the usage of this command.

        Example:

            files [--mode VAL] [paths]...

        .. versionchanged:: 0.1.3
           the `ignore_cmd` is renamed to `isdefault`.
        '''
        if isdefault:
            usage = '%s ' % sys.argv[0]
        else:
            usage = '%s %s ' % (sys.argv[0], self.name)
        for alias, real in self.opts.iteritems():
            hyphen = '-' * (1 + (len(alias) > 1))
            val = (' VAL', '')[isinstance(self.defaults.get(real, None), bool)]
            usage += '[%s%s%s] ' % (hyphen, alias, val)
        for argname in self.argnames[:-len(self.defaults) or None]:
            usage += '%s ' % argname.upper()
        if self.varname:
            usage += '[%s]... ' % self.varname
        return usage

    def help(self):
        '''Print help to stdout. Contains usage and the docstring of this
        function.'''

        print 'usage:', self.get_usage()
        if self.doc:
            print
            print self.doc

    def __call__(self, usrargs):
        '''Parse `usargs` and call the function.'''

        posargs, optargs = self.parse(usrargs)
        return self.func(*posargs, **optargs)

class Program(object):
    '''Convert a module, class or dict into multi-command CLI program.
    
    .. versionchanged:: 0.1.3
       Argument `module` is renamed to `obj`. The types it accpect is more
       specifically.

    .. versionchanged:: 0.1.3
       Use the name of default command, `defname` instead of `default`.
    
    .. versionadded:: 0.1.3
       Argument `doc`.'''

    def __init__(self, obj, defname=None, doc=None):

        if not isinstance(obj, dict):
            self.doc = doc or getdoc(obj)
            obj = dict( (name, getattr(obj, name)) for name in dir(obj) )
        else:
            self.doc = doc

        self.defname = defname

        self.cmds = {}
        for name, ref in obj.items():
            if not callable(ref)   : continue
            if name.startswith('_'): continue
            if inspect.isclass(ref): continue 

            self.cmds[name] = Command(ref, name=name)

        if len(self.cmds) == 1 and self.defname is None:
            self.defname = self.cmds.keys()[0]

    def get_cmds_usages(self):
        '''Return a list contains the usage of the functions in this program.'''
        return [ cmd.get_usage() for cmd in self.cmds.values() ]

    def get_tip(self, cmd=None):
        '''Return the 'Try ... for more information.' tip.
        
        .. versionchanged:: 0.1.3
           Take a command as argument instead of a function.'''

        target = sys.argv[0]
        if cmd:
            target += ' ' + cmd.name

        return 'Try `%s --help` for more information.' % target

    def help(self):
        '''Print the complete help of this program.'''

        usages = self.get_cmds_usages()
        if self.defname:
            usages.insert(0, self.cmds[self.defname].get_usage(isdefault=True))
        for i, usage in enumerate(usages):
            if i == 0:
                print 'usage:',
            else:
                print '   or:',
            print usage                

        if self.doc:
            print
            print self.doc

    def help_error(self, cmd=None):
        '''Print the tip.

        .. versionchanged:: 0.1.3
           Take a command as argument instead of a function.'''

        print self.get_tip(cmd)

    def __call__(self, usrargs):
        '''Use it as a CLI program.'''
        
        if not usrargs or usrargs[0] == '--help':
            self.help()
            return 0

        try:
            cmd = self.cmds[usrargs[0]]
        except KeyError:
            cmd = self.cmds.get(self.defname, None)
        else:
            usrargs.pop(0)

        if cmd is None:
            print '%s: No command \'%s\' found.' % (sys.argv[0], usrargs[0])
            self.help_error()
            return 2

        try:
            val = cmd(usrargs)
        except (getopt.GetoptError, TypeError), err:

            if hasattr(err, 'opt') and err.opt == 'help':
                cmd.help()
            else:
                print '%s: %s' % (sys.argv[0], str(err))
                self.help_error(cmd)

            return 2
        else:
            if val: print val
            return 0

def main(obj=None, defname=None, doc=None, exit=False):
    '''Use it to simply convert your program.

    `obj` is the target you want to convert. `obj` can be a moudle, a class
    or a dict. If `obj` is None, it uses the `__main__` module (the
    first-running Python program).
    
    `defname` is the name of default command, an attribute name or a key in
    `obj`.

    `doc` is the addational information you want to show on help. Use the
    docstring of `obj` by default.

    `exit`, True if you want to exit entire program after calling it.

    .. versionchanged:: 0.1.3
       Arguments `module` is renamed to `obj` and `default` is renamed to
       `defname` and changed the usage.

    .. versionadded:: 0.1.3
       Arguments `doc` and `exit`.
    '''

    prog = Program(obj or sys.modules['__main__'], defname, doc)
    status = prog(sys.argv[1:])
    if exit:
        sys.exit(status)
    else:
        return status

if __name__ == '__main__':

    def clime(target, *args):
        '''Dynamicly make a module or Python file into CLI program.

        `target` can be a moudle or Python file path.'''

        module = None

        try:
            module = __import__(target)
        except ImportError:
            pass

        try:
            module = {}
            execfile(target, module)
        except IOError, e:
            module = None
            print '%s: %s' % (sys.argv[0], e)

        if module:
            prog = Program(module)
            prog(sys.argv[2:])

    main({'clime': clime})
