# -*- coding:utf-8 -*-
import win32api
import win32con
import time

# 键盘扫描码映射表（硬件级，对应物理按键）
# 格式：字符: (按下扫描码, 释放扫描码, 是否需要Shift)
SCAN_CODE_MAP = {
    # 数字键（主键盘区）
    '0': (0x0B, 0x8B, True), '1': (0x02, 0x82, True),
    '2': (0x03, 0x83, True), '3': (0x04, 0x84, True),
    '4': (0x05, 0x85, True), '5': (0x06, 0x86, True),
    '6': (0x07, 0x87, True), '7': (0x08, 0x88, True),
    '8': (0x09, 0x89, True), '9': (0x0A, 0x8A, True),
    # 小写字母（无需Shift）
    'a': (0x1E, 0x9E, False), 'b': (0x30, 0xB0, False),
    'c': (0x2E, 0xAE, False), 'd': (0x20, 0xA0, False),
    'e': (0x12, 0x92, False), 'f': (0x21, 0xA1, False),
    'g': (0x22, 0xA2, False), 'h': (0x23, 0xA3, False),
    'i': (0x17, 0x97, False), 'j': (0x24, 0xA4, False),
    'k': (0x25, 0xA5, False), 'l': (0x26, 0xA6, False),
    'm': (0x32, 0xB2, False), 'n': (0x31, 0xB1, False),
    'o': (0x18, 0x98, False), 'p': (0x19, 0x99, False),
    'q': (0x10, 0x90, False), 'r': (0x13, 0x93, False),
    's': (0x1F, 0x9F, False), 't': (0x14, 0x94, False),
    'u': (0x16, 0x96, False), 'v': (0x2F, 0xAF, False),
    'w': (0x11, 0x91, False), 'x': (0x2D, 0xAD, False),
    'y': (0x15, 0x95, False), 'z': (0x2C, 0xAC, False),
    # 特殊键
    ' ': (0x39, 0xB9, False),  # 空格
    '\n': (0x1C, 0x9C, False),  # 回车
    'backspace': (0x0E, 0x8E, False),  # 退格
}


def press_scan_code(scan_code, is_press=True):
    """
    发送扫描码模拟按键（硬件级）
    :param scan_code: 扫描码
    :param is_press: True=按下，False=释放
    """
    if is_press:
        win32api.keybd_event(0, scan_code, 0, 0)
    else:
        win32api.keybd_event(0, scan_code, win32con.KEYEVENTF_SCANCODE, 0)
    time.sleep(0.02)  # 硬件按键间隔


def simulate_single_key(char):
    """模拟单个字符的按键操作"""
    # 大写字母转小写+Shift
    if char.isupper():
        char = char.lower()
        shift_needed = True
    else:
        shift_needed = SCAN_CODE_MAP.get(char, (0, 0, False))[2]

    # 获取扫描码
    press_code, release_code, _ = SCAN_CODE_MAP.get(char, (0, 0, False))
    if press_code == 0:
        print(f"暂不支持字符: {char}")
        return

    # 需要Shift则先按Shift
    if shift_needed:
        press_scan_code(0x2A, True)  # 左Shift按下

    # 按下并释放目标键
    press_scan_code(press_code, True)
    press_scan_code(release_code, False)

    # 释放Shift
    if shift_needed:
        press_scan_code(0xAA, False)  # 左Shift释放


def switch_to_chinese_input():
    """模拟切换到中文输入法（Ctrl+Shift）"""
    # 按下Ctrl+Shift
    press_scan_code(0x1D, True)  # 左Ctrl按下
    press_scan_code(0x36, True)  # 右Shift按下
    time.sleep(0.1)
    # 释放Ctrl+Shift
    press_scan_code(0xB6, False)  # 右Shift释放
    press_scan_code(0x9D, False)  # 左Ctrl释放
    time.sleep(0.5)  # 等待输入法切换完成


def input_chinese_by_pinyin(chinese_text, pinyin_list=None):
    """
    模拟输入中文（通过拼音+选字）
    :param chinese_text: 要输入的中文（如"大赛"）
    :param pinyin_list: 拼音列表（如["da", "sai"]），None则自动拆分
    """
    # 自动拆分拼音（简单版，复杂场景需手动指定）
    if pinyin_list is None:
        pinyin_map = {
            "大": "da", "赛": "sai", "测": "ce", "试": "shi",
            "和": "he", "我": "wo", "你": "ni", "他": "ta",
            "的": "de", "是": "shi", "在": "zai", "上": "shang"
        }
        pinyin_list = [pinyin_map.get(char, char) for char in chinese_text]

    for pinyin in pinyin_list:
        # 输入拼音字母
        for char in pinyin:
            simulate_single_key(char)
            time.sleep(0.05)
        # 按空格确认选字（默认选第一个候选词）
        simulate_single_key(' ')
        time.sleep(0.1)


def input_mixed_text(text_list):
    print(text_list)
    from lib.auto_input_text import auto_type
    import time

    # 3秒切换到输入框
    time.sleep(3)

    # 直接打中文
    auto_type(str(text_list))



if __name__ == '__main__':
    # 测试：混合输入数字、中文
    input_mixed_text([98498498, "大赛和测试123"])