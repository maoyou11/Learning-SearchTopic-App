# -*- coding:utf-8 -*-
# 创建孤儿线程

# Copyright (C) 2026 YourName
# Distributed under the GNU General Public License v3.0.
# See the LICENSE file in the project root for full license text.

import subprocess
import os
from threading import Thread
from conf.settings import *


def run_new_thread():
    # 获取当前脚本(main.py)所在的绝对目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # 拼接show/run.vbs的绝对路径（简化写法，和你原代码逻辑一致）
    program_path = DEANTICAPTURE_VBS_PATH

    print(program_path)

    if not os.path.exists(program_path):
        return

    # 1. 先检查文件是否存在（关键排查步骤）
    if not os.path.exists(program_path):
        return

    # 2. 尝试启动程序，并捕获异常（新增，排查启动失败原因）
    try:
        print(program_path)
        os.startfile(program_path)
    except Exception as e:
        print(f"❌ 启动失败：{str(e)}")


if __name__ == "__main__":
    run_new_thread()