# _*_coding : UTF_8 _*_

# Copyright (C) 2026 YourName
# Distributed under the GNU General Public License v3.0.
# See the LICENSE file in the project root for full license text.

import win32gui
import win32con


def get_all_windows_info():
    """列出所有可见窗口的句柄、标题、类名（用于定位目标窗口）"""
    windows_info = []

    def callback(handle, extra):
        if win32gui.IsWindowVisible(handle):
            title = win32gui.GetWindowText(handle)
            class_name = win32gui.GetClassName(handle)
            if title or class_name:  # 至少有标题或类名才记录
                windows_info.append({
                    "handle": handle,
                    "title": title,
                    "class_name": class_name
                })
                print(f"句柄：{handle} | 标题：[{title}] | 类名：{class_name}")
        return True

    win32gui.EnumWindows(callback, None)
    return windows_info


def hide_window_by_keyword(keyword, search_title=True, search_class=False):
    """
    隐藏指定特征的窗口（无需psutil）
    :param keyword: 匹配的关键词（标题或类名）
    :param search_title: 是否搜索标题
    :param search_class: 是否搜索类名
    """
    hidden_count = 0

    def callback(handle, extra):
        nonlocal hidden_count
        try:
            # 获取窗口标题和类名
            title = win32gui.GetWindowText(handle)
            class_name = win32gui.GetClassName(handle)

            # 判断是否匹配
            match = False
            if search_title and keyword in title:
                match = True
            if search_class and keyword in class_name:
                match = True

            if match:
                # 强制隐藏窗口（双重保障）
                win32gui.ShowWindow(handle, win32con.SW_HIDE)
                win32gui.SetWindowPos(
                    handle, 0, 0, 0, 0, 0,
                    win32con.SWP_HIDEWINDOW | win32con.SWP_NOSIZE | win32con.SWP_NOMOVE
                )
                hidden_count += 1
                print(f"已隐藏窗口：标题=[{title}] | 类名={class_name} | 句柄={handle}")
        except Exception as e:
            # 忽略无权限的系统窗口
            pass
        return True

    # 遍历所有窗口
    win32gui.EnumWindows(callback, None)

    # 反馈结果
    if hidden_count == 0:
        search_type = "标题" if search_title else "类名"
        print(f"未找到{search_type}包含「{keyword}」的窗口，请检查关键词是否正确")
    else:
        print(f"共隐藏 {hidden_count} 个匹配的窗口")


def show_window_by_handle(handle):
    """通过句柄精准恢复窗口"""
    try:
        win32gui.ShowWindow(handle, win32con.SW_SHOW)
        win32gui.SetWindowPos(
            handle, 0, 0, 0, 0, 0,
            win32con.SWP_SHOWWINDOW | win32con.SWP_NOSIZE | win32con.SWP_NOMOVE
        )
        title = win32gui.GetWindowText(handle)
        print(f"已恢复窗口：标题=[{title}] | 句柄={handle}")
    except Exception as e:
        print(f"恢复窗口失败：{e}")


# 主程序
if __name__ == "__main__":
    # 第一步：先列出所有窗口信息，找到DeAntiCapture的准确特征
    print("=== 所有可见窗口信息 ===")
    windows = get_all_windows_info()

    # 第二步：隐藏目标窗口（根据实际查到的关键词调整）
    print("\n=== 开始隐藏窗口 ===")
    # 方式1：按标题匹配（优先尝试）
    # hide_window_by_keyword("反反截屏软件,ShareBit(QQ:82170290)", search_title=True, search_class=False)

    # 方式2：如果标题匹配不到，按类名匹配（替换为实际查到的类名）
    # hide_window_by_keyword("DeAntiCaptureClass", search_title=False, search_class=True)

    # 方式3：如果知道句柄，直接隐藏（替换为实际查到的句柄）
    target_handle = 2032372  # 替换为真实句柄
    win32gui.ShowWindow(target_handle, win32con.SW_HIDE)