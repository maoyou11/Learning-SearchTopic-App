# -*- coding:utf-8 -*-
import os.path
import subprocess
import time
from conf.settings import *

def auto_type(text: str):

    if (not os.path.exists(AHK_EXE)) or (not os.path.exists(AHK_SCRIPT)):
        print("AHK_EXE AHK_SCRIPT 文件不存在")

    """调用AHK自动打字，支持中文，不使用剪贴板"""
    # 命令格式：AutoHotkey64.exe 脚本.ahk "要输入的文字"
    cmd = [
        AHK_EXE,
        AHK_SCRIPT,
        text
    ]

    time.sleep(3)

    # 静默运行，不弹出黑窗口
    subprocess.Popen(
        cmd,
        creationflags=subprocess.CREATE_NO_WINDOW
    )


# 测试调用
if __name__ == "__main__":
    auto_type("你好，Python调用AHK无剪贴打字测试 123ABC，支持中文！")
