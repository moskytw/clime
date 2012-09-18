#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: noet sts=4:ts=4:sw=4
# author: takano32 <tak@no32 dot tk>
#

def clime_dirname(file_name):
	if suffix == None:
		pass
	else:
		pass
	print("basename")

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

