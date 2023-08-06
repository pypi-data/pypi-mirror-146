import os

def cmd(command):
    sc1 = os.system(command)
    sc2 = os.popen(command).read()
    if sc1 == 0:
        print("执行成功！")
    else:
        print("执行中发生了错误！")

def help(command='all'):
    if command == 'all':
        print("帮助文档-cmd:")
        print("导入:  from pyCDTT")
        print("执行cmd指令:  pyCDTT.cmd.cmd(cmd指令)")
        print("帮助:  pyCDTT.cmd.help(命令)\n注：如果想查看cmd下的所有命令的话，输入:  pyCDTT.cmd.help()  或  在括弧里输入'all'")
    else:
        if command == 'import':
            print("帮助文档-cmd-import:")
            print("导入:  from pyCDTT")
        else:
            if command == 'cmd':
                print("帮助文档-cmd-cmd:")
                print("执行cmd指令:  pyCDTT.cmd.cmd(cmd指令)")
            else:
                if command == 'help':
                    print("帮助文档-cmd-help:")
                    print("帮助:  pyCDTT.cmd.help(命令)\n注：如果想查看cmd下的所有命令的话，输入:  pyCDTT.cmd.help()  或  在括弧里输入'all'")
                else:
                    print("pyCDTT：[错误]没有名为" + command + "的命令")