#!/usr/bin/python
# -*- encoding: utf-8 -*-
# -*- 使用 UTF-8 编码 -*-
# winrun client for cygwin.

import sys, os, subprocess
import socket


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

	
class WinRunClient:
	def __init__(self):
		self.kwargs = {}
		self.shortcutDir = "/home/shortcut/config"
		
	def _initServerAddress(self):
		varBase = "/var/run/winrun/winrun-server"
		for e in ["ip", "port"]:
			with open(varBase + "." + e, "rb") as f:
				setattr(self, e, f.read())
		self.port = int(self.port)
		print "server ip: %s, port: %d" % (self.ip, self.port)
		
	def _initCwd(self):
		self.kwargs["cwd"] = getWinPath(os.getcwd())
		
	def _initCommand(self):
		self.command = sys.argv[0]
		if os.path.basename(self.command).startswith("winrun"):
			if len(sys.argv) <= 1:
				raise RuntimeError("missing command. usage: winrun command [args...]")
			# command 为 winrun 的第一个参数
			self.command = sys.argv[1]
			self.args = sys.argv[1:]
		else:
			# 使用 winrun 中的命令调用, command 设置为命令名
			self.command = os.path.basename(sys.argv[0])
			self.args = [self.command] + sys.argv[1:]
		#print "command: %s, args: %s" % (repr(self.command), repr(self.args))

	def _initExecutable(self):
		path = None
		shortcut = os.path.join(self.shortcutDir, self.command)
		# 使用 shortcut 定位文件
		if self.command.find('/') < 0:
			if os.path.exists(shortcut):
				path = shortcut
		# 通过命令路径定位文件
		elif os.path.isfile(self.command):
			path = self.command
		# 如果找到文件，设置 executable
		if path is not None:
			# 如果是 win7 符号连接, 先定位到实际路径
			path = os.path.realpath(path)
			winpath = getWinPath(path)
			self.args[0] = winpath
			self.kwargs["executable"] = winpath
			print "executable:", winpath
		# 否则不设置 executable
		else:
			print "executable: (use command %s)" % repr(self.command)
			
	def _initArgs(self):
		"""构造启动应用程序的参数列表.
		如果一个参数包含 '/'，并且这个参数的前缀是一个已存在的路径，
		则将此参数转换为 windows 路径。
		因为 '/' 必然存在，所有以 '/' 开头的参数都将被转换。
		"""
		args = []
		for e in self.args:
			pos = e.find('/')
			if pos >= 0 and os.path.exists(e[:pos + 1]):
				args.append(getWinPath(e))
			else:
				args.append(e)
		self.kwargs["args"] = args

	def _sendRequest(self):
		request = repr(self.kwargs)
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try: 
			sock.connect((self.ip, self.port))
			sock.sendall(request)
			# 服务器接收命令以 "\n" 结束
			sock.sendall("\n")
			response = sock.recv(1024)
		finally:
			sock.close()
		#print "send request: %s, response: %s." % (request, response)
		# for simplier output.
		print "args: %s\nresponse: %s." % (repr(self.kwargs["args"]), response)
		
	def main(self):
		self._initServerAddress()
		self._initCwd()
		self._initCommand()
		self._initExecutable()
		self._initArgs()
		self._sendRequest()

		
if __name__ == '__main__':
	WinRunClient().main()
