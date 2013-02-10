#!/usr/bin/python
# -*- encoding: utf-8 -*-
# -*- 编码: utf-8 -*-

import os, subprocess

import winrun

"""winrun for cygwin.
在 cygwin 下调用 windows 命令行工具时，自动进行参数转换。
"""

def getWinPath(path):
	"""转换路径格式为 windows 路径。
	通过调用 "cygpath -w" 实现。
	"""
	p = subprocess.Popen(["cygpath", "-w", path], stdout=subprocess.PIPE)
	out, err = p.communicate()
	if not err:
		winpath = out.strip()
	#print "convert to winpath. from: %s, to: %s." % tuple(repr(e) for e in (path, winpath))
	else:
		winpath = path
	#print "conver to winpath failed. path: %s, out: %s, err: %s" % tuple(repr(e) for e in (path, out, err))
	return winpath


def convertArgument(e):
	"""转换命令行参数.
	转换规则：
	1. 如果一个参数以 "//" 开头，则将开头的 "//" 转成 "/"，其他不变。
	2. 否则，如果一个参数以 "/", "./" 或 "../" 开头，
	   则认为是一个 cygwin 格式的文件路径，则将其转换为 windows 格式。
	3. 否则，不做任何转换。
	"""
	if e.startswith("//"):
		e = e[1:]
	elif e.startswith("/") or e.startswith("./") or e.startswith("../"):
		e = getWinPath(e)
	return e


def getAlternativeExecutableByWhich(command):
	out = subprocess.check_output(["which", "-a", command]).strip().splitlines()
	if len(out) > 1:
		return out[1]


class WinRunCyg(winrun.WinRun):
	def main(self):
		self.init()
		# 在 cygwin 中执行时，如果没有找到 executable，将导致循环调用。
		# 尝试通过 which 查找候选 executable.
		if not self.executable:
			self.executable = getAlternativeExecutableByWhich(self.command)
		if not self.executable:
			raise RuntimeError("executable not found. command: " + self.command)
		print "executable: %s\nargs: %s" % (self.executable, self.args)
		os.execvp(self.executable or self.args[0], self.args)

	def initConfigDir(self):
		"""在 cygwin 下, 启动器的目录更深一层, configDir 相对要再向上一层."""
		super(WinRunCyg, self).initConfigDir()
		# 调整 configDir 相对向上一层
		path, name = os.path.split(self.configDir)
		path = os.path.dirname(path)
		self.configDir = os.path.join(path, name)

	def initCommand(self):
		"""在 cygwin 中调用时，转换命令行参数。"""
		super(WinRunCyg, self).initCommand()
		self.args = [convertArgument(e) for e in self.args]

if __name__ == '__main__':
	WinRunCyg().main()
