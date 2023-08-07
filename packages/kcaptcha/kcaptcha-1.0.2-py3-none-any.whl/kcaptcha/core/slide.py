# --coding:utf-8--
import io

import cv2
import numpy as np
from PIL import Image, ImageChops

from kcaptcha.tools import pil_to_cv2


class SlideKiller(object):
    @classmethod
    def get_target(cls, img_bytes: bytes = None):
        image = Image.open(io.BytesIO(img_bytes))
        w, h = image.size
        start_x = 0
        start_y = 0
        end_x = 0
        end_y = 0
        for x in range(w):
            for y in range(h):
                p = image.getpixel((x, y))
                if p[-1] == 0:
                    if start_y != 0 and end_y == 0:
                        end_y = y

                    if start_x != 0 and end_x == 0:
                        end_x = x
                else:
                    if start_y == 0:
                        start_y = y
                        end_y = 0
                    else:
                        if y < start_y:
                            start_y = y
                            end_y = 0
            if start_x == 0 and start_y != 0:
                start_x = x
            if end_y != 0:
                end_x = x
        return image.crop([start_x, start_y, end_x, end_y]), start_x, start_y

    def match(self, target_bytes: bytes = None, background_bytes: bytes = None, simple_target: bool = True,
              debug: bool = False,
              method: int = cv2.TM_CCOEFF_NORMED,
              target_threshold=(100, 120),
              background_threshold=(100, 300),
              border=False):
        """
        :param target_bytes: 拼图块的bytes
        :param background_bytes: 背景图的bytes
        :param simple_target: 拼图块是否有背景
        :param debug: 是否启动debug模式，开启后将返回识别过程中产生的图片（以N纬数组的形式返回）
        :param method: 进行匹配所用的算法： cv2.TM_CCOEFF = 4 （系数匹配法）
                                        cv2.TM_CCOEFF_NORMED = 5（相关系数匹配法）
                                        cv2.TM_CCORR = 2 （相关匹配法）
                                        cv2.TM_CCORR_NORMED = 3 （归一化相关匹配法）
                                        cv2.TM_SQDIFF = 0 （平方差匹配法）
                                        cv2.TM_SQDIFF_NORMED = 1 （归一化平方差匹配法）

        :param target_threshold: 二值化拼图块的阈值二元组，当结果频繁错误时调整此项。
        :param background_threshold: 二值化背景图片的阈值二元组，当结果频繁错误时调整此项。
        :param border: 是否对target块增加边框以提升准确率
        :return:
        """

        if not simple_target:
            target, target_x, target_y = self.get_target(target_bytes)
            target = cv2.cvtColor(np.asarray(target), cv2.IMREAD_ANYCOLOR)
        else:
            target = cv2.imdecode(np.frombuffer(target_bytes, np.uint8), cv2.IMREAD_ANYCOLOR)
            target_y = 0

        background = cv2.imdecode(np.frombuffer(background_bytes, np.uint8), cv2.IMREAD_ANYCOLOR)

        target = cv2.Canny(target, target_threshold[0], target_threshold[1])

        if border:
            # target块增加1像素的白色边框，使匹配更准确
            target = cv2.copyMakeBorder(target, 1, 1, 1, 1, borderType=cv2.BORDER_CONSTANT, value=(255, 255, 255))

        background = cv2.Canny(background, background_threshold[0], background_threshold[1])
        background = cv2.cvtColor(background, cv2.COLOR_GRAY2RGB)
        target = cv2.cvtColor(target, cv2.COLOR_GRAY2RGB)

        res = cv2.matchTemplate(background, target, method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        h, w = target.shape[:2]
        top_left = (int(max_loc[0]), int(max_loc[1]))
        bottom_right = (max_loc[0] + w, max_loc[1] + h)

        data = {
            "target_y": target_y,
            "target": [int(top_left[0]), int(top_left[1]), int(bottom_right[0]), int(bottom_right[1])],
        }
        if debug:
            result = background.copy()
            cv2.rectangle(result, top_left, bottom_right, (0, 0, 255), 2)
            cv2.imshow('Target', target)
            cv2.imshow('Bg', result)
            cv2.waitKey()

        return data

    @classmethod
    def compare(cls, background_bytes: bytes = None, full_background_bytes: bytes = None,
                threshold: int = 80, debug: bool = False):
        bg_img = Image.open(io.BytesIO(background_bytes)).convert("RGB")
        full_bg_img = Image.open(io.BytesIO(full_background_bytes)).convert("RGB")
        diff_image = ImageChops.difference(full_bg_img, bg_img)
        bg_img.close()
        full_bg_img.close()
        image = diff_image.point(lambda x: 255 if x > threshold else 0)
        start_y = 0
        start_x = 0
        for i in range(0, image.width):
            count = 0
            for j in range(0, image.height):
                pixel = image.getpixel((i, j))
                if pixel != (0, 0, 0):
                    count += 1
                if count >= 5 and start_y == 0:
                    start_y = j - 5

            if count >= 5:
                start_x = i + 2
                break

        data = {
            "target": [start_x, start_y]
        }
        if debug:
            diff_image_cv2 = pil_to_cv2(diff_image)
            image_cv2 = pil_to_cv2(image)
            cv2.imshow('Difference', diff_image_cv2)
            cv2.imshow('Result', image_cv2)
            cv2.waitKey()

        return data


def test_slide_match():
    slide_killer = SlideKiller()
    # test slide match mode
    with open('../imgs/slide_match_target_1.jpg', 'rb') as f:
        test_match_target = f.read()
    with open('../imgs/slide_match_bg_1.jpg', 'rb') as f:
        test_match_background = f.read()
    match_result = slide_killer.match(test_match_target, test_match_background, simple_target=True,
                                      target_threshold=(200, 300),
                                      method=cv2.TM_CCOEFF,
                                      background_threshold=(100, 200), debug=True, border=True)
    print(match_result)


def test_slide_compare():
    slide_killer = SlideKiller()
    with open('../imgs/slide_compare_bg_1.png', 'rb') as f:
        test_compare_bg = f.read()

    with open('../imgs/slide_compare_full_bg_1.png', 'rb') as f:
        test_compare_full_bg = f.read()

    compare_result = slide_killer.compare(background_bytes=test_compare_bg,
                                          full_background_bytes=test_compare_full_bg,
                                          debug=True, threshold=50)
    print(compare_result)


if __name__ == '__main__':
    test_slide_match()
    test_slide_compare()
    # test slide compare mode
    pass
