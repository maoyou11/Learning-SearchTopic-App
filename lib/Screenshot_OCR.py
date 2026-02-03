# -*- coding:utf-8 -*-
import pyautogui

from lib.OCR import ocr_options


def select_area_ocr(app_id, api_key, secret_key):
    # 全屏截图
    fullscreen_ocr(0, "./image/screen.png")

    if not (app_id and api_key and secret_key):
        return ""

    # 截取图片
    ocr_options()

    # 手动追加cmd里的所有参数，和你测试成功的命令完全一致
    # 识别
    text = get_text("./image/title.png", app_id, api_key, secret_key)

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


# 全屏截图
def fullscreen_ocr(delay=3, save_path="c.png"):
    """
    延迟全屏截图并进行OCR识别
    :param delay: 延迟秒数（默认3秒，给你准备时间切换窗口）
    :param save_path: 全屏截图保存路径（默认：c.png）
    :return: 清洗后的识别文本
    """
    pyautogui.sleep(delay)

    # 调用新增的独立全屏截图函数
    fullscreen_img = capture_fullscreen(save_path)


def capture_fullscreen(save_path="fullscreen.png"):
    """
    捕获整个屏幕并保存到指定路径
    :param save_path: 全屏截图的保存路径（默认：fullscreen.png）
    :return: 全屏截图的PIL Image对象（方便后续OCR或其他处理）
    """
    try:
        # 捕获全屏
        fullscreen_img = pyautogui.screenshot()
        # 保存截图到本地
        fullscreen_img.save(save_path)
        return fullscreen_img
    except Exception as e:
        print(f"❌ 全屏截图失败：{str(e)}")
        return None


# 调用测试
def run(app_id=None, api_key=None, secret_key=None):
    # 调用鼠标框选识别（核心功能，无任何报错）
    select_text = select_area_ocr(str(app_id), str(api_key), str(secret_key))

    if "下一步" in select_text:
        return select_text, True

    # 打印识别结果
    return select_text if select_text else "识别失败\n", False


if __name__ == '__main__':
    run()