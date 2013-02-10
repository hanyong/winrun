#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# -*- 编码: utf-8 -*-

"""winrun for windows 7.
windows 7 下的 windows 应用程序启动器。
"""

import sys, os, subprocess

def getFinalPathName(path):
	"""调用 winapi 获取文件最终路径."""
	import win32file, win32con

	f = win32file.CreateFile(path,
		win32file.GENERIC_READ,
		win32file.FILE_SHARE_READ,
		None,
		win32file.OPEN_EXISTING,
		win32file.FILE_ATTRIBUTE_NORMAL,
		None)
	try:
		path = win32file.GetFinalPathNameByHandle(f, win32con.FILE_NAME_NORMALIZED)
		# 为了保持最好的兼容性，去掉返回路径中的 r"\\?\" 前缀.
		prefix = r"\\?\ ".strip()
		if path.startswith(prefix):
			path = path[len(prefix):]
	finally:
		win32file.CloseHandle(f)
	return path


class WinRun(object):
	def __init__(self):
		self.name = None
		self.configDir = None
		self.command = None
		self.executable = None
		self.args = None

	def main(self):
		self.init()
		print "executable: %s\nargs: %s" % (self.executable, self.args)
		# 在 windows 上, exec() 有 bug, subprocess.call() 感觉更好.
		subprocess.call(self.args, executable=self.executable)

	def init(self):
		self.initName()
		self.initConfigDir()
		self.initCommand()
		self.initExecutable()

	def initName(self):
		self.name = "winrun"

	def initConfigDir(self):
		filePath = os.path.abspath(sys.argv[0])
		fileDir = os.path.dirname(filePath)
		self.configDir = os.path.join(fileDir, "config")

	def initCommand(self):
		filename = os.path.basename(sys.argv[0])
		self.command = os.path.splitext(filename)[0]
		if self.command == self.name:
			# 通过 self.name 显式调用时, command 直接等于 sys.argv[1]
			if len(sys.argv) <= 1:
				raise RuntimeError("missing command. usage: %s command [args...]" % self.name)
			self.command = sys.argv[1]
			self.args = sys.argv[1:]
		else:
			# 否则, command 等于基本命令名
			self.args = [self.command] + sys.argv[1:]

	def initExecutable(self):
		"""设置 command 对应的可执行文件路径.
		如果不存在对应的可执行文件，则 self.executable 保持不变（默认为 None）.
		"""
		if self.command.find(os.path.sep) < 0:
			shortcut = os.path.join(self.configDir, self.command)
			if os.path.islink(shortcut):
				self.executable = os.path.realpath(shortcut)
			# 如果 python 未正确识别 windows symlink, 调用 winapi 获取文件最终路径
			elif os.path.isfile(shortcut):
				self.executable = getFinalPathName(shortcut)
		elif os.path.isfile(self.command):
			self.executable = os.path.realpath(self.command)

if __name__ == '__main__':
	WinRun().main()
