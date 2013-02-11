winrun
======

windows 程序启动器。帮助命令行用户在 cygwin 下调用 windows 程序，如 "notepad++ /tmp/1.c", "explorer ~" 等。

安装使用说明
===

安装前本机 win7 系统和 cygwin 都需要分别安装 python 2.7，本机 win7 还需要安装 pywin32。
以下步骤如果没有特殊说明，均在 cygwin 下执行。

1. clone 代码到一个目录下，进入代码目录。安装过程只是创建符号连接，因此安装完成后代码目录需要继续保留。

        git clone git://github.com/hanyong/winrun.git
        cd winrun

1. 执行安装脚本 winrun-setup.py，接受一个参数，表示安装路径。下面以安装到 /home/shortcut 目录下为例。

        python winrun-setup.py /home/shortcut

1. 按照提示编辑 .bash_profile 添加路径到 PATH，注意 cygwin 下必须添加到 PATH 的前面。
按照提示修改 win7 环境变量 PATH 添加路径，建议添加到 PATH 后面即可。修改 win7 环境变量 PATHEXT，添加 ";PY;PYW"。
重启 windows 命令提示符和 cygwin。

1. 在 windows 下按 Win + R，输入 "winrun-server.py" 或 "winrun-server" （设置了 PATHEXT），启动 winrun-server。
    
        winrun-server

1. 在 cygwin 下执行 winrun-add 添加启动器。启动器有两种。
    1. 一种是已经在 windows 下的 PATH 中存在的程序，希望在 cygwin 下执行时添加一层包装，如转换参数等，
        此时用 "winrun-add 命令名" 即可。以添加 notepad 为例。

            winrun-add notepad          
                
        添加完成后调用 notepad 即可自动转换 cygwin 路径参数，如 "notepad ~/1.c" 即可打开主文件下的文件。
    1. 一种是不在 PATH 中存在的程序，此时需要两个参数，用 "winrun-add 命令名 路径"。
        第二个参数为可执行文件完整路径，结尾的 ".exe" 后缀不可省略。
        以添加 notepad++ 为例，notepad++ 在我本机的完整路径为 "/d/opt/notepad++/notepad++.exe"。
    
            winrun-add npp /d/opt/notepad++/notepad++.exe
        
        添加完成后通过 npp 即可启动 notepad++，并且可以自动转换 cygwin 路径参数。

注意
===
- 在 cygwin 下，默认情况下，命令行程序通过 winrun 启动，不依赖 winrun-server，
GUI 程序通过 winrunclient 启动，需要依赖 winrun-server。

- 在 windows 下，命令行程序使用 ".py" 后缀，GUI程序使用 ".pyw" 后缀，均不依赖 winrun-server。
