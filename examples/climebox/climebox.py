#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: noet sts=4:ts=4:sw=4
# author: takano32 <tak@no32 dot tk>
#

def clime_dirname(file_name):
	# NOTE os.path.dirname
	# http://www.python.jp/doc/2.4/lib/module-os.path.html
	print("dirname")

def clime_foo():
	pass

if __name__ == '__main__':
	import clime
	import sys, os
	cmdname = os.path.basename(sys.argv[0])
	print(cmdname)
	for cmdnames in clime.Program().cmdfs.keys():
		print(cmdnames)
	# import clime.now

	# NOTE exec
	# http://docs.python.org/library/os.html?highlight=exec#os.execve

