# --coding:utf-8--
import cv2
import numpy as np

from loguru import logger

from kcaptcha.core import OcrKiller, ClickKiller

ORC = OcrKiller()
CLICK = ClickKiller()


def click_in_order(img_bytes: bytes, debug=False, ocr=ORC, click=CLICK):
    # 首先进行目标识别，获得所有文字的目标区域
    det_result = click.detection(img_bytes=img_bytes)
    img_buffer_numpy = np.frombuffer(img_bytes, dtype=np.uint8)
    img = cv2.imdecode(img_buffer_numpy, 1)

    # 结果分两部分：主区域待点击部分及副区域语序部分
    # 1.对主区域部分进行切割得到文字块后通过ocr进行文字识别
    main_area_boxes = [x for x in det_result[:len(det_result) // 2]]
    main_area_results = {}
    for box in main_area_boxes:
        x1, y1, x2, y2 = box
        char_img = img[y1:y2, x1:x2]
        encode_result, encoded_img = cv2.imencode('.jpg', char_img)
        char = ocr.classification(encoded_img.tobytes())
        main_area_results[char] = box

    # 2.对语序部分按x坐标排序后进行ocr识别，再和主区域对应
    sort_area_boxes = [x for x in det_result[len(det_result) // 2:]]

    # TODO: 这里两部分识别出的字符数可能不一样
    # assert len(main_area_boxes) == len(sort_area_boxes)

    sort_area_boxes.sort(key=lambda x: x[0])
    not_matched_box = {}
    match_results = [{}] * len(sort_area_boxes)
    for i, box in enumerate(sort_area_boxes):
        x1, y1, x2, y2 = box
        char_img = img[y1:y2, x1:x2]
        encode_result, encoded_img = cv2.imencode('.jpg', char_img)
        char = ocr.classification(encoded_img.tobytes())

        if not char:
            continue

        if main_area_results.get(char):
            main_area_box = main_area_results.pop(char)
            match_results[i] = {'char': char, 'target': main_area_box}

        else:
            if not_matched_box:
                return None

            else:
                not_matched_box = {'index': i, 'name': char}

    if not_matched_box:
        if len(main_area_results) > 1:
            return None

        else:
            for char, box in main_area_results.items():
                match_results[not_matched_box['index']] = {'char': char, 'target': box}

    match_results = [x for x in match_results if x]

    if debug:
        for each_result in match_results:
            x1, y1, x2, y2 = each_result['target']
            cv2.rectangle(img, (x1, y1), (x2, y2), color=(0, 0, 255), thickness=2)
            cv2.imshow('Result', img)
            cv2.waitKey()

    return match_results


def test_all():
    import os

    success_count = 0
    fail_count = 0

    for index, each in enumerate(os.listdir('../tests/click/')):
        with open(f'../tests/click/{each}', 'rb') as f:
            data = f.read()

        try:
            results = click_in_order(data)
            if results:
                text = ''.join(x['char'] for x in results)
                success_count += 1
            else:
                text = None
                fail_count += 1

            print(f'{success_count}/{fail_count}', text, results)

        except Exception as e:
            logger.exception(e)

    print(f'成功：{success_count}，失败：{fail_count}，成功率：{success_count / (fail_count + success_count) * 100}')


def test():
    with open('../imgs/geetest_click_1.png', 'rb') as f:
        img_bytes = f.read()

    result = click_in_order(img_bytes, debug=True)
    print(result)


if __name__ == '__main__':
    # test_all()
    test()
    pass
