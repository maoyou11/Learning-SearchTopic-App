# -*- coding:utf-8 -*-

import cv2
import numpy as np

from conf.settings import *

options = None
screen_left_top_deviation = []
screen_right_bottom_end_point = []


def image_init(image):
    # 导入图片
    image_a = cv2.imread(IMAGE_A_PATH)
    image_b = cv2.imread(IMAGE_B_PATH)
    image_c = cv2.imread(IMAGE_C_PATH)
    image_d = cv2.imread(IMAGE_D_PATH)
    image_next = cv2.imread(IMAGE_NEXT_PATH)

    # 选项字典
    global options
    options = {
        "A": image_a,
        "B": image_b,
        "C": image_c,
        "D": image_d,
        "next": image_next,
    }

    # 配置
    height, width = image.shape[:-1]

    padding_left = 280
    padding_right = 279
    padding_top = 165
    padding_bottom = 40

    # start_width_than = 0.14583333333333334
    # end_width_than = 0.8546875
    # start_height_than = 0.1527777777777778
    # end_height_than = 0.9629629629629629

    start_width_than = padding_left/width
    end_width_than = (width-padding_right)/width
    start_height_than = padding_top/height
    end_height_than = (height-padding_bottom)/height

    start_width = int(start_width_than*width)
    end_width = int(end_width_than*width)
    start_height = int(start_height_than*height)
    end_height = int(end_height_than*height)

    global screen_left_top_deviation, screen_right_bottom_end_point
    screen_left_top_deviation = [start_width, start_height]
    screen_right_bottom_end_point = [end_width, end_height]

    return options


def find_options(gray_image, template):
    start_width, start_height = screen_left_top_deviation

    # 获取模板宽高
    h, w = template.shape[:2]

    # 计算相似度
    res = cv2.matchTemplate(gray_image, template, 1)

    # 找到全局的最小值、最大值，以及这两个值对应的坐标位置
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    # 计算终点坐标
    start_w_h = min_loc[0] + start_width, min_loc[1] + start_height
    end_w_h = start_w_h[0] + w, start_w_h[1] + h
    # 统一转为NumPy数组计算，避免类型差异
    p1 = np.array(start_w_h, dtype=np.float32)
    p2 = np.array(end_w_h, dtype=np.float32)
    mid_x_float, mid_y_float = ((p1 + p2) / 2.0)
    midpoint = tuple(map(int, [mid_x_float, mid_y_float]))

    return midpoint, (start_w_h, end_w_h)


def ocr_options(correct_options=""):
    image = cv2.imread(IMAGE_SCREEN_PATH)

    options = image_init(image)

    start_width, start_height = screen_left_top_deviation
    end_width, end_height = screen_right_bottom_end_point

    # 截取图像
    cat = image[start_height:end_height, start_width:end_width]
    gray_cat = cv2.cvtColor(cat, cv2.COLOR_BGR2GRAY)

    cv2.imwrite(IMAGE_TITLE_PATH, cat)

    if not correct_options:
        return None

    # 设置盒大小(腐蚀精度) 值越大腐蚀越大
    kernel = np.ones((3, 3), np.uint8)
    # 腐蚀操作 (图像对象, 盒, 迭代次数)
    # 迭代次数=重复腐蚀次数
    gray_cat = cv2.erode(gray_cat, kernel, iterations=1)

    # 选项灰度
    gray_options = cv2.cvtColor(options.get(correct_options), cv2.COLOR_BGR2GRAY)

    midpoint, (start_w_h, end_w_h) = find_options(gray_cat, gray_options)

    save_painting_result("options", start_w_h, end_w_h)

    return midpoint


def ocr_next():
    image = cv2.imread(IMAGE_TITLE_PATH)
    # 匹配下一题
    next_point, (start_w_h, end_w_h) = find_options(image, options.get("next"))

    print((start_w_h, end_w_h))
    save_painting_result("screen_next", start_w_h, end_w_h)

    return next_point


def save_painting_result(image_name, start_w_h, end_w_h):
    image = cv2.imread(IMAGE_SCREEN_PATH)
    # 画矩形
    cv2.rectangle(image, start_w_h, end_w_h, (0, 0, 255), 2)
    # cv2.imshow(f"{image_name}.png", test_image)
    cv2.imwrite(os.path.join(IMAGE_PATH, f"{image_name}.png"), image)


if __name__ == '__main__':
    ocr_options("A")