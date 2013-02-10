# winrun server for windows.

import sys, os
import SocketServer
import subprocess
import traceback
import time

def _now():
	return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

class WinRunServer:
	def __init__(self):
		self._initVarBase()
		with open(self.varBase + ".pid", "wb") as f:
			f.write(str(os.getpid()))
	def _initVarBase(self):
		if len(sys.argv) > 1 and os.path.isdir(sys.argv[1]):
			varPath = sys.argv[1]
		else:
			varPath = r'D:\cygwin\var\run'
		varPath = os.path.join(varPath, "winrun")
		if not os.path.exists(varPath):
			os.makedirs(varPath)
		self.varBase = os.path.join(varPath, "winrun-server")	
	def main(self):
		host, port = "localhost", 0
		server = SocketServer.TCPServer((host, port), WinRunHandler)
		ip, port = server.server_address
		for e in ["ip", "port"]:
			with open(self.varBase + "." + e, "wb") as f:
				f.write(str(eval(e)))
		print _now(), "winrun-server ready. listening ip: %s, port: %d." % (ip, port)
		server.serve_forever()

class WinRunHandler(SocketServer.StreamRequestHandler):
	def handle(self):
		ip = self.client_address[0]
		data = self.rfile.readline().strip()
		print _now(), "clientIp: %s, data: %s." % (ip, data),
		try:
			kwargs = eval(data)
			p = subprocess.Popen(creationflags=subprocess.CREATE_NEW_CONSOLE, **kwargs)
			#p = subprocess.Popen(**kwargs)
			msg = "ok. pid: %d." % p.pid
		except:
			msg = "ERROR!"
			traceback.print_exc()
		finally:
			self.wfile.write(msg)
			print msg
		
if __name__ == '__main__':
	WinRunServer().main()
