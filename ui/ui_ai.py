# _*_coding : UTF_8 _*_
# author : SJYssr
# Date : 2024/12/26 下午10:17
# ClassName : ui_ai.py
# Github : https://github.com/SJYssr
# 用途：AI界面控件的创建、布局、AI搜索与输入事件处理。
import sys
import tkinter as tk


def create_ai_ui(root, on_back, on_ai_search, on_input, on_screenshot, text_size=10):
    """
    创建AI界面控件并布局，返回控件引用字典。
    :param root: Tk主窗口
    :param on_back: 返回按钮回调
    :param on_ai_search: AI搜索按钮回调
    :param on_input: 输入按钮回调
    :param on_screenshot: 截图按钮回调 (新增：绑定你的OCR框选识别函数)
    :param text_size: 初始字体大小
    :return: dict
    """
    ai_frame = tk.Frame(root)
    # 顶部搜索框
    ai_search_frame = tk.Frame(ai_frame)
    ai_search_frame.pack(side="top", fill="x")
    ai_search_entry = tk.Entry(ai_search_frame)
    ai_search_entry.pack(side="left", fill="x", expand=True, padx=5, pady=5)
    ai_search_entry.configure(foreground='gray')

    # 顶部搜索框 回车触发AI搜索 原有绑定保留
    ai_search_entry.bind("<Return>", lambda event: on_ai_search())

    # 顶部按钮
    back_button = tk.Button(ai_search_frame, text="返回", command=on_back)
    back_button.pack(side="right", padx=5, pady=5)
    back_button.configure(foreground='gray')
    ai_search_button = tk.Button(ai_search_frame, text="AI搜索", command=on_ai_search)
    ai_search_button.pack(side="right", padx=5, pady=5)
    ai_search_button.configure(foreground='gray')

    # 截图按钮
    screenshot_button = tk.Button(ai_search_frame, text="截图", command=on_screenshot)
    screenshot_button.pack(side="right", padx=5, pady=5)
    screenshot_button.configure(foreground='gray')

    # 快捷键截图
    # 方式1：绑定【F2】快捷键触发截图，推荐！全局通用、无冲突
    ai_frame.bind("<x>", lambda event: on_screenshot())
    # 绑定快捷键给主窗口root，确保焦点不在界面上也能触发（双重保险）
    root.bind("<x>", lambda event: on_screenshot())

    # 方式1：绑定【F2】快捷键触发截图，推荐！全局通用、无冲突
    ai_frame.bind("1", lambda event: on_screenshot())
    # 绑定快捷键给主窗口root，确保焦点不在界面上也能触发（双重保险）
    root.bind("1", lambda event: on_screenshot())

    # 方式1：绑定【F2】快捷键触发截图，推荐！全局通用、无冲突
    ai_frame.bind("<F2>", lambda event: on_screenshot())
    # 绑定快捷键给主窗口root，确保焦点不在界面上也能触发（双重保险）
    root.bind("<F2>", lambda event: on_screenshot())

    # 改用 bind_all 绑定给整个应用
    root.bind_all("<Button-3>", lambda event: on_screenshot())


    # 快捷键退出
    ai_frame.bind("<F6>", lambda event: sys.exit())
    root.bind("<F6>", lambda event: sys.exit())

    # 中间文本框
    ai_text_box = tk.Text(ai_frame, wrap="word", font=("Arial", text_size))
    ai_text_box.pack(fill="both", expand=True)
    ai_text_box.configure(foreground='gray')

    # 底部输入框和按钮
    ai_bottom_frame = tk.Frame(ai_frame)
    ai_bottom_frame.pack(side="bottom", fill="x")
    ai_input_entry = tk.Entry(ai_bottom_frame)
    ai_input_entry.pack(side="left", fill="x", expand=True, padx=5, pady=5)
    ai_input_entry.configure(foreground='gray')
    ai_submit_button = tk.Button(ai_bottom_frame, text="输入", command=lambda: on_input(ai_input_entry))
    ai_submit_button.pack(side="right", padx=5, pady=5)
    ai_submit_button.configure(foreground='gray')

    # 返回控件对象
    return {
        'ai_frame': ai_frame,
        'ai_search_frame': ai_search_frame,
        'ai_search_entry': ai_search_entry,
        'back_button': back_button,
        'ai_search_button': ai_search_button,
        'screenshot_button': screenshot_button,
        'ai_text_box': ai_text_box,
        'ai_input_entry': ai_input_entry,
        'ai_submit_button': ai_submit_button,
        'ai_bottom_frame': ai_bottom_frame
    }