# _*_coding : UTF_8 _*_
# author : SJYssr
# Date : 2024/12/26 下午10:17
# ClassName : main.py
# Github : https://github.com/SJYssr
# 用途：程序主入口，负责加载配置、初始化界面、事件绑定、AI调用与主流程调度。

import _thread as thread
import time

import pyautogui
from pynput.keyboard import Controller
from conf.config_manager import load_config_if_exists, save_deepseek_config
from ai_API.ai_spark import Ws_Param, on_error, on_close, on_open, run, on_message
from ai_API.ai_deepseek import call_deepseek_api
from lib.auto_input_text import auto_type
from lib.utils import set_window_on_top, change_opacity, change_opacity0, close_window, change_weight
from ui.ui_main import create_main_ui, highlight_search, next_search_result
from ui.ui_ai import create_ai_ui
from lib.Screenshot_OCR import run as ocr_run
import ssl
import websocket
import functools
from lib.input_text import input_mixed_text
from lib.OCR import ocr_options, ocr_next
from conf.settings import *
from ui.ui_settings import create_settings_embedded
from ui.ui_tk import TkMainUi
import tkinter as tk
from openai import OpenAI


class Auto_click(TkMainUi):
    def __init__(self):
        super().__init__()

        self.MODE = "TEST"
        self.is_small = False  # 窗口大小状态

        self.load_config()
        self.on_change_weight()

    # 事件处理函数
    def start_move(self, event):
        """鼠标按下，记录窗口当前位置"""
        self.x = event.x
        self.y = event.y

    # 鼠标拖动，移动窗口
    def stop_move(self, event):
        """鼠标拖动，移动窗口"""
        self.root.geometry(f"+{event.x_root - self.x}+{event.y_root - self.y}")

    # Ctrl + 滚轮调整字体大小
    def change_text_size(self, event):
        """Ctrl+滚轮调整字体大小"""
        global text_size
        text_size = max(10, min(text_size, 12))
        if self.main_ui['main_frame'].winfo_ismapped():
            if event.delta > 0:
                text_size += 1
            else:
                text_size -= 1
            self.main_ui['text_box'].config(font=("Arial", text_size))
        elif self.ai_ui['ai_frame'].winfo_ismapped():
            if event.delta > 0:
                text_size += 1
            else:
                text_size -= 1
            self.ai_ui['ai_text_box'].config(font=("Arial", text_size))

    # F3切换窗口大小
    def on_change_weight(self, *args):
        """F3切换窗口大小"""
        self.is_small, self.current_opacity = change_weight(self.root, self.is_small, self.current_opacity)

    # Ctrl + 滚轮调整窗口透明度
    def on_change_opacity(self, event):
        """Ctrl+滚轮调整窗口透明度"""
        self.current_opacity = change_opacity(event, self.root, self.current_opacity, self.is_small)

    # 右键切换窗口透明度
    def on_change_opacity0(self, event):
        """右键切换窗口透明度"""
        self.current_opacity = change_opacity0(self.root, self.current_opacity, self.is_small)

    # 切换到AI界面
    def on_ai_button(self):
        """切换到AI界面"""
        self.main_ui['search_frame'].pack_forget()
        self.main_ui['main_frame'].pack_forget()
        self.ai_ui['ai_frame'].pack(fill="both", expand=True)

    # 切换回主界面
    def on_back(self):
        """切换回主界面"""
        # 隐藏AI或设置界面
        if self.ai_ui['ai_frame'].winfo_ismapped():
            self.ai_ui['ai_frame'].pack_forget()
        if hasattr(self, "settings_ui") and self.settings_ui['settings_frame'].winfo_ismapped():
            self.settings_ui['settings_frame'].pack_forget()
        # 显示主界面
        self.main_ui['search_frame'].pack(side="top", fill="x")
        self.main_ui['main_frame'].pack(fill="both", expand=True)

    # 主界面搜索高亮
    def on_search(self):
        """主界面搜索高亮"""
        highlight_search(self.main_ui['text_box'], self.main_ui['search_entry'])

    # 主界面输入自动打字
    def on_input(self, entry):
        """主界面输入自动打字"""
        input_text = entry.get()
        if not input_text:
            return

        thread.start_new_thread(self.input_thread, ())

    # 更新AI搜索框内容
    def update_ai_text(self, content):
        self.ai_ui['ai_text_box'].config(state='normal')
        # ai_ui['ai_text_box'].delete('1.0', tk.END)  # 回答前先清空
        self.ai_ui['ai_text_box'].insert(tk.END, "\n" + content)
        self.ai_ui['ai_text_box'].config(state='disabled')

    # AI搜索
    def run_ai(self):
        try:
            if self.type == 1:
                wsParam = Ws_Param(self.appid, self.api_key, self.api_secret, self.Spark_url)
                websocket.enableTrace(False)
                wsUrl = wsParam.create_url()
                query = self.ai_ui['ai_search_entry'].get()

                ws = websocket.WebSocketApp(
                    wsUrl,                               on_message=functools.partial(
                        on_message, ai_text_box=self.ai_ui['ai_text_box'],             update_ai_text=self.update_ai_text, root=self.root
                    ),
                    on_error=functools.partial(
                        on_error,
                        update_ai_text=self.update_ai_text
                    ),
                    on_close=functools.partial(
                        on_close,
                        update_ai_text=self.update_ai_text
                    ),
                    on_open=
                    lambda ws: on_open(
                        ws,
                        lambda ws: run(ws, self.appid, query, self.domain)
                    )
                )

                ws.appid = self.appid
                ws.query = query
                ws.domain = self.domain
                ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})

            elif self.type == 2:
                if hasattr(self, "search_text"):
                    search_text = self.search_text
                else:
                    search_text = self.ai_ui['ai_search_entry'].get()

                response = call_deepseek_api(self.deepseek_ai_client, search_text, self.deepseek_model)

                # 三元运算符

                self.root.after(0, lambda: self.update_ai_text(response if response else  ""))

                # 显示结果
                self.show_options(response.strip())

        except Exception as e:
            print(f"发生错误: {str(e)}")
            pass
        finally:
            self.root.after(0, lambda: self.ai_ui['ai_search_button'].config(state='normal'))

    # AI界面AI搜索，支持讯飞星火和Deepseek
    def on_ai_search(self):
        """AI界面AI搜索，支持讯飞星火和Deepseek"""
        self.ai_ui['ai_search_button'].config(state='disabled')
        # 仅在Deepseek时展示占位提示；讯飞星火不显示
        if self.type == 2:
            self.ai_ui['ai_text_box'].config(state='normal')
            # ai_ui['ai_text_box'].delete('1.0', tk.END)
            self.ai_ui['ai_text_box'].insert(tk.END, "\n" + "正在思考中，请稍候...")
            self.ai_ui['ai_text_box'].config(state='disabled')

        thread.start_new_thread(self.run_ai, ())

    # AI界面输入自动打字
    def on_ai_input(self, entry):
        """AI界面输入自动打字"""
        self.input_text = entry.get()
        if not self.input_text:
            return

        thread.start_new_thread(self.input_thread, ())

    # 自动打字
    def input_thread(self):
        keyboard = Controller()
        time.sleep(1)
        keyboard.type(self.input_text)
        time.sleep(0.5)
        # entry.delete(0, 'end')

    # 截图识别
    def on_screenshot(self):
        # 调用你的OCR识别函数，拿到识别的文字
        self.search_text, is_end = ocr_run(self.app_id, self.api_key, self.secret_key)

        # self.update_ai_text(f"{self.search_text[:20]}... {is_end}\n")

        if not self.search_text:
            return

        # ai搜索
        self.on_ai_search()

        if is_end:
            return

        # self.root.after(9000, self.on_screenshot)

    def release_mouse_capture(self):
        """释放 Win32 鼠标捕获，不改变窗口样式"""

        import ctypes
        # 1. 发送 WM_CANCELMODE 消息，取消窗口的模态捕获
        ctypes.windll.user32.SendMessageW(
            self.root.winfo_id(), 0x001F, 0, 0
        )
        # 2. 释放鼠标捕获
        ctypes.windll.user32.ReleaseCapture()
        # 3. 短暂改变透明度，强制窗口让出焦点后再恢复
        self.root.attributes("-alpha", 0.99)
        self.root.update()
        self.root.attributes("-alpha", 1.00)
        time.sleep(0.1)

    # 点击输入答案
    def show_options(self, ai_answer_all: str):

        # 移动鼠标
        options = ai_answer_all.split("#")

        import re
        if not bool(re.search("[abcdABCD]", ai_answer_all)):
            # 输入填空题答案
            # return
            auto_type(*options)

        # 选择题
        for option in options:
            # 鼠标移动
            # move_abcd().get(option[0])()

            # 点击答案
            midpoint = ocr_options(option[0])

            self.release_mouse_capture()

            # 2. 左键单击（默认就是左键，无需额外配置）
            pyautogui.click(*midpoint, duration=1)
            time.sleep(0.05)

        # 点击下一个
        midpoint = ocr_next()
        # 1. 移动鼠标
        pyautogui.moveTo(*midpoint, 1)
        # 2. 左键单击（默认就是左键，无需额外配置）
        pyautogui.click()
        time.sleep(0.05)

    # 保存设置界面API回调函数
    def on_save(self, api_key_value, model_value):
        try:
            if not api_key_value.strip():
                return
            save_deepseek_config(api_key_value.strip(), (model_value or 'deepseek-chat').strip())
            # 热切换到Deepseek
            deepseek_api_key = api_key_value.strip()
            deepseek_model = (model_value or 'deepseek-chat').strip()
            type = 2
        except Exception:
            return

    # 加载配置
    def load_config(self):
        # 加载配置（若无则使用写死的讯飞星火默认配置，不创建文件）
        self.config = load_config_if_exists()

        # deepseek config
        self.deepseek_config = (self.config or {}).get('deepseek', {})
        self.deepseek_api_key = self.deepseek_config.get('api_key', "")
        self.deepseek_model = self.deepseek_config.get('model', "")

        # OCR config
        self.ocr_config = (self.config or {}).get('ocr', {})
        self.app_id = self.ocr_config.get('app_id', "")
        self.api_key = self.ocr_config.get('api_key', "")
        self.secret_key = self.ocr_config.get('secret_key', "")

        if self.deepseek_api_key:
            # 使用Deepseek
            self.type = 2
        else:
            # 使用写死的讯飞星火
            self.type = 1
            self.appid = "1b69309b"
            self.api_secret = "YWY0MWJhNTM4MGU3NTJkZDJiMDM0ZjZl"
            self.api_key = "5b2302f3ac2295e56bd13f587d7ffa6e"
            self.Spark_url = "wss://spark-api.xf-yun.com/v1.1/chat"
            self.domain = "lite"

    def init_client(self):
        # 初始化 DeepSeek 客户端
        self.deepseek_ai_client = OpenAI(
            api_key=self.config["deepseek"]["api_key"],
            base_url="https://api.deepseek.com"  # 官方标准 Base URL
        )

    # 启动
    def start(self):

        # 启动窗口置顶
        set_window_on_top(self.root)

        self.init_client()

        # 启动主循环
        self.root.mainloop()


def main_run():
    app = Auto_click()
    app.start()






