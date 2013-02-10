#!/usr/bin/python
# -*- encoding: utf-8 -*-
# -*- 编码: utf-8 -*-

import os
import socket

from winruncyg import WinRunCyg, getWinPath

"""winrun client for cygwin.
在 cygwin 下调用，自动进行参数转换后将命令传送到 winrun-server 运行。
"""

class WinRunClient(WinRunCyg):
	def __init__(self):
		super(WinRunClient, self).__init__()
		self.varBase = "/var/run/winrun/winrun-server"
		self.ip = "127.0.0.1"
		self.port = None
		self.cwd = None

	def main(self):
		self.init()
		print "executable: %s\nargs: %s" % (self.executable, self.args)
		self.sendRequest()

	def init(self):
		super(WinRunClient, self).init()
		self.initCwd()
		self.initServerAddress()

	def initName(self):
		self.name = "winrunclient"

	def initExecutable(self):
		"""传递给 windows 运行时, 将 executable 路径转换成 windows 格式."""
		super(WinRunCyg, self).initExecutable()
		if self.executable:
			self.executable = getWinPath(self.executable)

	def initCwd(self):
		self.cwd = getWinPath(os.getcwd())

	def initServerAddress(self):
		for e in ["ip", "port"]:
			with open(self.varBase + "." + e, "rb") as f:
				setattr(self, e, f.read())
		self.port = int(self.port)
		print "server ip: %s, port: %d" % (self.ip, self.port)

	def sendRequest(self):
		kwargs = { }
		for e in ["cwd", "executable", "args"]:
			kwargs[e] = getattr(self, e)
		request = repr(kwargs)
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			sock.connect((self.ip, self.port))
			sock.sendall(request)
			# 服务器接收命令以 "\n" 结束
			sock.sendall("\n")
			response = sock.recv(1024)
		finally:
			sock.close()
		print "response: %s." % response

if __name__ == '__main__':
	WinRunClient().main()
