import os
import shutil

def del_file(path):
    os.remove(path)

def del_folder(path):
    shutil.rmtree(path)

def help(command='all'):
    if command == 'all':
        print("帮助文档-del:")
        print("导入:  from pyCDTT")
        print("删除单个文件:  pyCDTT.del.del_file(文件路径)")
        print("删除文件夹与文件夹下的所有文件:  pyCDTT.del.del_folder(文件夹路径)")
        print("帮助:  pyCDTT.del.help(命令)\n注：如果想查看del下的所有命令的话，输入:  pyCDTT.del.help()  或  在括弧里输入'all'")
    else:
        if command == 'import':
            print("帮助文档-del-import:")
            print("导入:  from pyCDTT")
        else:
            if command == 'del_file':
                print("帮助文档-del-del_files:")
                print("删除单个文件:  pyCDTT.del.del_file(文件路径)")
            else:
                if command == 'del_folder':
                    print("帮助文档-del-del_folder:")
                    print("删除文件夹与文件夹下的所有文件:  pyCDTT.del.del_folder(文件夹路径)")
                else:
                    if command == 'help':
                        print("帮助文档-del-help:")
                        print("帮助:  pyCDTT.del.help(命令)\n注：如果想查看del下的所有命令的话，输入:  pyCDTT.del.help()  或  在括弧里输入'all'")
                    else:
                        print("pyCDTT：[错误]没有名为" + command + "的命令")