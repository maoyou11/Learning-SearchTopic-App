# -*- coding:utf-8 -*-


# Copyright (C) 2026 YourName
# Distributed under the GNU General Public License v3.0.
# See the LICENSE file in the project root for full license text.
import tkinter as tk
from ui.ui_ai import create_ai_ui
from ui.ui_settings import create_settings_embedded
from ui.ui_main import create_main_ui, next_search_result


class TkMainUi:
    def __init__(self):
        # 全局状态变量
        self.current_opacity = 0.5  # 窗口透明度
        self.text_size = 10  # 字体大小

        self.SetUi()
        self.SetKey()
        pass

    def SetUi(self):
        # 初始化主窗口和界面
        self.root = tk.Tk()
        self.root.geometry("300x533+0+380")
        self.root.attributes("-alpha", self.current_opacity)
        self.root.configure(bg='white')
        self.root.overrideredirect(True)

        # 创建主界面、AI界面与（懒加载）设置界面
        self.main_ui = create_main_ui(self.root, self.on_ai_button, self.on_search, self.on_input, self.text_size, on_settings=self.open_settings)

        self.ai_ui = create_ai_ui(self.root, self.on_back, self.on_ai_search, self.on_ai_input, self.on_screenshot, self.text_size)

        self.ai_ui['ai_frame'].pack_forget()

    def SetKey(self):
        # 事件绑定
        self.root.bind("<Control-Button-1>", self.start_move)
        self.root.bind("<Control-B1-Motion>", self.stop_move)
        self.root.bind("<F3>", self.on_change_weight)
        self.root.bind("<Button-3>", self.on_change_opacity0)
        self.root.bind("<Control-MouseWheel>", self.on_change_opacity)
        self.root.bind("<Alt-MouseWheel>", self.change_text_size)
        self.root.bind("<Escape>", lambda e: self.close_window(e, self.root))
        self.root.bind("<Return>", lambda e: next_search_result(self.main_ui['text_box']))
        self.root.bind("<Escape>", lambda e: next_search_result(self.main_ui['text_box']))

    # 打开设置界面
    def open_settings(self):

        # 如果尚未创建，先创建嵌入式设置界面
        if not hasattr(self, "settings_ui"):
            self.settings_ui = create_settings_embedded(
                self.root,
                self.on_save,
                self.on_back,
                self.text_size,
                default_api_key=self.deepseek_api_key,
                default_model=self.deepseek_model
            )
        else:
            # 已创建则更新默认显示（覆盖原值）
            try:
                self.settings_ui['api_entry'].delete(0, tk.END)

                if self.deepseek_api_key:
                    self.settings_ui['api_entry'].insert(0, self.deepseek_api_key)

                self.settings_ui['model_entry'].set(self.deepseek_model)
            except Exception:
                pass
        # 切换显示
        if self.main_ui['search_frame'].winfo_ismapped():
            self.main_ui['search_frame'].pack_forget()
        if self.main_ui['main_frame'].winfo_ismapped():
            self.main_ui['main_frame'].pack_forget()
        if self.ai_ui['ai_frame'].winfo_ismapped():
            self.ai_ui['ai_frame'].pack_forget()
        self.settings_ui['settings_frame'].pack(fill="both", expand=True)
