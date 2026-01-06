# -*- coding:utf-8 -*-
from pynput.keyboard import Controller, Key
import time


def input_text(text_to_input: list):
    keyboard = Controller()
    delay_before_start = 3  # 切换到输入框的时间（秒）
    char_interval = 0.05  # 字符输入间隔（模拟人工）

    for text_input in text_to_input:
        time.sleep(delay_before_start)
        text_input = str(text_input)
        for char in text_input:
            if char == '\n':
                keyboard.press(Key.enter)
                keyboard.release(Key.enter)
            else:
                keyboard.press(char)
                keyboard.release(char)
            time.sleep(char_interval)


if __name__ == '__main__':
    input_text([98498498])