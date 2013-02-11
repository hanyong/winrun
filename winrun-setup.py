#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# -*- 编码: utf-8 -*-

import sys, os, subprocess

__author__ = 'hanyong'

"""在 cygwin 下安装启动器到指定目录。
1. 确认安装目录存在。
2. 创建 config, cygwin 目录。
3. 在 cygwin 目录创建 winruncyg.py 和 winrunclient.py 的 cygwin 符号连接。
4. 在 cygwin 目录添加 cmd 的启动器。
5. 在安装目录创建 winrun.py 的 windows 符号连接。
用户可在安装目录创建符号链接创建自己的启动器。
"""

def main():
	instDir = sys.argv[1]
	print u"创建安装目录..."
	subprocess.call(["mkdir", "-p", instDir])
	configDir = os.path.join(instDir, "config")
	cygwinDir = os.path.join(instDir, "cygwin")
	for e in [configDir, cygwinDir]:
		subprocess.call(["mkdir", "-p", e])
	selfDir = os.path.abspath(os.path.dirname(sys.argv[0]))
	# 设置所有 python 脚本为可执行.
	os.chdir(selfDir)
	subprocess.call('chmod +x *.py', shell=True)
	print u"创建 cygwin 下 winrun 符号连接..."
	subprocess.call(["ln", "-sf", os.path.join(selfDir, "winruncyg.py"), os.path.join(cygwinDir, "winrun")])
	subprocess.call(["ln", "-sf", os.path.join(selfDir, "winrunclient.py"), os.path.join(cygwinDir, "winrunclient")])
	subprocess.call(["ln", "-sf", os.path.join(selfDir, "winrun-add.py"), os.path.join(cygwinDir, "winrun-add")])
	print u"为了能在 cygwin 中调用启动器，请在 cygwin 的 PATH 前面添加："
	print "\t" + cygwinDir
	os.environ["PATH"] = os.path.pathsep.join([cygwinDir, os.environ["PATH"]])
	print u"添加 cygwin 启动器 ..."
	for e in ["cmd", "explorer"]:
		subprocess.call(["ln", "-sf", "winrunclient", os.path.join(cygwinDir, e)])
	print u"创建 windows 下 winrun.py 符号连接"
	for e in ["winrun.py", "winrun-server.py"]:
		target = os.path.join(instDir, e)
		if os.path.islink(target) or os.path.exists(target):
			os.remove(target)
		subprocess.call(["winrun", "cmd", "//c", "mklink", target, os.path.join(selfDir, e)])
	print u"为了能在 windows 中调用启动器，请在 windows 的 PATH 中添加："
	print "\t" + subprocess.check_output(["cygpath", "-w", instDir]).strip()
	print u'为了方便在 windows 命令提示符下调用启动器（python脚本），请在 windows 的 PATHEXT 添加 ";PY;PYW"'
	print u"为了方便在 cygwin 下创建 windows 符号连接，建议在 .bashrc 中设置："
	print """\talias mklink='winrun cmd //c mklink'"""


if __name__ == '__main__':
	main()
