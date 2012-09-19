#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: noet sts=4:ts=4:sw=4
# author: takano32 <tak@no32 dot tk>
#

def climebox_dirname(file_name):
	# http://www.python.jp/doc/2.4/lib/module-os.path.html
	print(os.path.dirname(file_name))

def climebox_foo():
	pass

if __name__ == '__main__':
	import clime
	import sys, os
	import inspect
	execname = os.path.basename(sys.argv[0])

	import __main__
	for cmdname in clime.Program().cmdfs.keys():
		attr = getattr(__main__, cmdname)
		cmdname = 'climebox_' + execname
		if cmdname == attr.func_name:
			clime.Program(defcmdname = cmdname, progname = execname).main()

