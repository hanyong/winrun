#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# -*- 编码：utf-8 -*-

import os
import subprocess
import sys

"""添加启动器。
usage:
	winrun-add name [path]
windows 下默认为 console 程序使用 ".py", GUI 程序使用 ".pyw".
cygwin 下默认为 console 程序使用 "winrun", GUI 程序使用 "winrunclient".
"""

__author__ = 'hanyong'

class WinRunAdd(object):
	def main(self):
		cygwinDir = os.path.abspath(os.path.dirname(sys.argv[0]))
		instDir = os.path.dirname(cygwinDir)
		configDir = os.path.join(instDir, "config")

		name = sys.argv[1]
		cygOnly = True
		if len(sys.argv) > 2:
			cygOnly = False
			path = sys.argv[2]
		else:
			try:
				path = subprocess.check_output(["which", "-a", name]).strip().splitlines()[-1]
			except:
				raise RuntimeError("executable for command not found: " + name)

		gui = True
		fileOut = subprocess.check_output(["file", path])
		if fileOut.find("executable (console)") >= 0:
			gui = False
		elif fileOut.find("executable (GUI)") >= 0:
			gui = True
		else:
			raise RuntimeError("file is not a executable: " + path)

		if not cygOnly:
			print "mklink:", name
			os.chdir(configDir)
			subprocess.call(["winrun", "cmd", "//c", "mklink", name, path])
			target = name + (gui and ".pyw" or ".py")
			print "mklink", target
			os.chdir(instDir)
			subprocess.call(["winrun", "cmd", "//c", "mklink", target, "winrun.py"])

		src = gui and "winrunclient" or "winrun"
		print ("ln %s:" % src), name
		os.chdir(cygwinDir)
		subprocess.call(["ln", "-sf", src, name])
		print "add shortcut done:", name

if __name__ == '__main__':
	WinRunAdd().main()
