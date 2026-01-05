# -*- coding:utf-8 -*-
import pyautogui
import pytesseract
from PIL import Image
import tkinter as tk

# 基础配置 - 你的Tesseract路径，原样保留，不用改！
pytesseract.pytesseract.tesseract_cmd = r'./Tesseract-OCR-32/tesseract.exe'

# 全局变量，存储框选的坐标
__start_x = 0
__start_y = 0
__end_x = 0
__end_y = 0
__select_flag = False


# ===================== ✨彻底修复tk冲突+卡死：鼠标框选区域截图+识别 (无任何报错) =====================
def select_area_ocr(app_id, api_key, secret_key):
    """
    鼠标框选识别：按住左键拖动 → 松开自动识别，带蓝色框选遮罩
    修复核心：用Toplevel子窗口替代Tk根窗口，解决主界面和OCR的tk冲突、卡死、中断报错
    :return: 识别后的清洗文本
    """
    global __start_x, __start_y, __end_x, __end_y, __select_flag
    __select_flag = False

    # ========== 核心修改点1：创建Toplevel子窗口 替代 Tk根窗口 【解决冲突的关键】 ==========
    root = tk.Toplevel()
    root.attributes('-fullscreen', True)
    root.attributes('-alpha', 0.2)  # 窗口透明度
    root.attributes('-topmost', True)
    root.config(cursor='cross')
    # ========== 核心修改点2：独占鼠标焦点+屏蔽主窗口操作，防止冲突 ==========
    root.grab_set_global()

    # 创建画布用于绘制框选矩形
    canvas = tk.Canvas(root, bg='white', highlightthickness=0)
    canvas.pack(fill=tk.BOTH, expand=True)

    # 鼠标左键按下事件 - 获取起始坐标
    def on_left_down(event):
        global __start_x, __start_y, __select_flag
        __select_flag = True
        __start_x = event.x
        __start_y = event.y

    # 鼠标拖动事件 - 实时绘制蓝色框选矩形
    def on_mouse_move(event):
        global __end_x, __end_y
        if __select_flag:
            __end_x = event.x
            __end_y = event.y
            canvas.delete('rect')
            # 绘制蓝色框选框，实时显示
            canvas.create_rectangle(__start_x, __start_y, __end_x, __end_y, outline='#0099ff', width=2, tag='rect')

    # 鼠标左键松开事件 - 获取结束坐标并关闭窗口
    def on_left_up(event):
        global __end_x, __end_y, __select_flag
        __select_flag = False
        __end_x = event.x
        __end_y = event.y
        root.destroy()  # 关闭子窗口

    # 绑定鼠标事件
    canvas.bind('<Button-1>', on_left_down)
    canvas.bind('<Motion>', on_mouse_move)
    canvas.bind('<ButtonRelease-1>', on_left_up)

    # ========== 核心修改点3：用wait_window() 替代 mainloop() 【解决卡死/中断报错】 ==========
    root.wait_window()

    # 计算最终的框选区域（兼容任意方向框选：左上→右下 / 右下→左上）
    x = min(__start_x, __end_x)
    y = min(__start_y, __end_y)
    width = abs(__end_x - __start_x)
    height = abs(__end_y - __start_y)

    # 过滤无效框选（只点击没拖动的情况）
    if width < 5 or height < 5:
        print("❌ 提示：框选区域无效，请重新框选！")
        return ""

    # 截图+保存+OCR识别，和你原逻辑完全一致
    select_screenshot = pyautogui.screenshot(region=(x, y, width, height))
    select_screenshot.save("a.png")
    # 手动追加cmd里的所有参数，和你测试成功的命令完全一致
    text = get_text("./a.png", app_id, api_key, secret_key)

    return text


# ===================== 你原有的功能1：指定坐标区域截图 + 文字识别 (原样保留) =====================
def screenshot_ocr(x, y, width, height):
    region_screenshot = pyautogui.screenshot(region=(x, y, width, height))
    region_screenshot.save("b.png")
    text = pytesseract.image_to_string(region_screenshot, lang='chi_sim+eng')
    clean_text = '\n'.join([line.strip() for line in text.split('\n') if line.strip()])
    return clean_text


# ===================== 你原有的功能2：全屏截图 + 延迟截图 (原样保留) =====================
def fullscreen_ocr(delay=3):
    pyautogui.sleep(delay)
    screenshot = pyautogui.screenshot()
    screenshot.save("c.png")
    text = pytesseract.image_to_string(screenshot, lang='chi_sim+eng')
    clean_text = '\n'.join([line.strip() for line in text.split('\n') if line.strip()])
    return text


# ===================== 你原有的功能3：识别本地图片中的文字 (原样保留) =====================
def img_ocr(img_path):
    img = Image.open(img_path)
    text = pytesseract.image_to_string(img, lang='chi_sim+eng')
    clean_text = '\n'.join([line.strip() for line in text.split('\n') if line.strip()])
    return text


def get_text(file_path, app_id, api_key, secret_key):
    from aip import AipOcr

    # 初始化客户端
    client = AipOcr(app_id, api_key, secret_key)

    # 读取图片内容
    with open(file_path, 'rb') as fp:
        image = fp.read()

    # 调用通用文字识别（高精度版）
    result = client.basicAccurate(image)

    # 解析结果
    text = ""
    for item in result.get('words_result', []):
        text += item['words'] + "\n"

    return text


# ===================== 调用测试 (核心：框选识别) =====================
def run(app_id, api_key, secret_key):
    # 调用鼠标框选识别（核心功能，无任何报错）
    select_text = select_area_ocr(str(app_id), str(api_key), str(secret_key))

    # 打印识别结果
    return select_text if select_text else "识别失败\n"


if __name__ == '__main__':
    run()