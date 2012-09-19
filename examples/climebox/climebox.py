#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: noet sts=4:ts=4:sw=4
# author: takano32 <tak@no32 dot tk>
#

def climebox_usage():
	# TODO: default command
	clime.Program().printusage()

def climebox_dirname(file_name):
	# http://docs.python.org/release/2.7.3/library/os.path.html#module-os.path
	print(os.path.dirname(file_name))

def climebox_false():
	exit(1)

def climebox_pwd():
	# http://docs.python.org/release/2.7.3/library/os.path.html#module-os.path
	print(os.getcwd())

if __name__ == '__main__':
	import clime
	import sys, os
	import inspect
	execname = os.path.basename(sys.argv[0])

	if execname == 'climebox' or execname == 'climebox.py':
		clime.Program(defcmdname = 'climebox_usage').main()
		exit(0)

	import __main__
	for cmdname in clime.Program().cmdfs.keys():
		attr = getattr(__main__, cmdname)
		cmdname = 'climebox_' + execname
		if cmdname == attr.func_name:
			clime.Program(defcmdname = cmdname, progname = execname).main()


