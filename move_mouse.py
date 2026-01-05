# -*- coding:utf-8 -*-
import pyautogui

length = 100

def move_mouse(dx, dy, time):
    # 获取当前鼠标的绝对坐标 → 返回 (x, y) 元组
    x, y = pyautogui.position()
    # 1.5秒内缓慢移动到目标点
    pyautogui.moveTo(x+dx-length/2, y+dy-length/2, duration=time)


def move_a():
    move_mouse(0, 0, 1.5)


def move_b():
    move_mouse(length, 0, 1.5)


def move_c():
    move_mouse(0, length, 1.5)


def move_d():
    move_mouse(length, length, 1.5)


def move_abcd():
    return {
        "A": move_a,
        "B": move_b,
        "C": move_c,
        "D": move_d,
    }


if __name__ == '__main__':
    move_abcd().get("A")()


