#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# -*- 编码: utf-8 -*-

"""winrun for windows 7."""

import sys, os, subprocess

class WinRun():
	def __init__(self):
		self.configDir = None
		
	def main(self):
		filepath = os.path.abspath(sys.argv[0])
		filedir = os.path.dirname(filepath)
		self.configDir = os.path.join(os.path.dirname(filedir), "config")
		
		filename = os.path.basename(sys.argv[0])
		command = os.path.splitext(filename)[0]
		if command == "winrun":
			# 通过 winrun 显式调用时, command 直接等于 sys.argv[1]
			command = sys.argv[1]
			args = sys.argv[1:]
		else:
			# 不是通过 winrun 显式调用时, command 等于基本命令名
			args = [command] + sys.argv[1:]
			
		executable = self.getExecutable(command)
		print "executable: %s\nargs: %s" % (executable, args)

		if os.name != "nt":
			# 在其他系统上, exec() 的行为非常适合作为启动器.
			os.execvp(executable or args[0], args)			
		else:
			# 在 windows 上, exec() 有 bug, subprocess.call() 感觉更好.
			subprocess.call(args, executable=executable)
		
	def getExecutable(self, command):
		path = None
		if command.find(os.path.sep) < 0:
			shortcut = os.path.join(self.configDir, command)
			if os.path.islink(shortcut):
				path = os.path.realpath(shortcut)
			elif os.path.isfile(shortcut):
				# 如果 python 未正确识别 windows symlink, 调用 winapi 获取最终文件路径
				import win32file, win32con
				f = win32file.CreateFile(shortcut,
						win32file.GENERIC_READ, 
						win32file.FILE_SHARE_READ, 
						None, 
						win32file.OPEN_EXISTING, 
						win32file.FILE_ATTRIBUTE_NORMAL, 
						None)
				try:
					path = win32file.GetFinalPathNameByHandle(f, win32con.FILE_NAME_NORMALIZED)
				finally:
					win32file.CloseHandle(f)
		elif os.path.isfile(command):
			path = command
		if path is not None:
			path = os.path.realpath(path)
		return path
	
if __name__ == '__main__':
	WinRun().main()
