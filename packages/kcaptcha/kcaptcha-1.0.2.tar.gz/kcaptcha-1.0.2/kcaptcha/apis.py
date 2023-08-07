# encoding=utf-8
import argparse
import base64
import json

from flask import Flask, request

from kcaptcha.core import ClickKiller, SlideKiller, OcrKiller
from kcaptcha.geetest import click_in_order

parser = argparse.ArgumentParser(description="验证码识别")
parser.add_argument("-p", "--port", type=int, default=9898)
parser.add_argument("--ocr", action="store_true", help="开启ocr识别")
parser.add_argument("--old", action="store_true", help="OCR是否启动旧模型")
parser.add_argument("--det", action="store_true", help="开启目标检测")

args = parser.parse_args()

app = Flask(__name__)


class Server(object):
    def __init__(self):
        self.click_killer = ClickKiller()
        self.ocr_killer = OcrKiller()
        self.slide_killer = SlideKiller()

    def classification(self, img: bytes):
        try:
            return self.ocr_killer.classification(img)
        except:
            raise Exception('Ocr识别失败')

    def detection(self, img: bytes):
        try:
            return self.click_killer.detection(img)
        except:
            raise Exception('目标检测失败')

    def slide_match(self, target_img: bytes, bg_img: bytes, **kwargs):
        return self.slide_killer.match(target_img, bg_img, **kwargs)

    def slide_compare(self, bg_img: bytes, full_bg_img: bytes):
        return self.slide_killer.compare(bg_img, full_bg_img)


server = Server()


def get_img(request, img_type='file', img_name='image'):
    if img_type == 'b64':
        img = base64.b64decode(request.get_data())  #
        try:  # json str of multiple images
            dic = json.loads(img)
            img = base64.b64decode(dic.get(img_name).encode())
        except Exception as e:  # just base64 of single image
            pass
    else:
        img = request.files.get(img_name).read()
    return img


def set_ret(result):
    if isinstance(result, Exception):
        return json.dumps({"code": 401, "results": "", "msg": str(result)}, ensure_ascii=False)
    else:

        return json.dumps({"code": 200, "results": result or [], "msg": ""}, ensure_ascii=False)


@app.route('/common/<opt>/<img_type>', methods=['POST'])
def ocr(opt, img_type='file'):
    try:
        img = get_img(request, img_type, 'img')
        if opt == 'ocr':
            result = server.classification(img)
        elif opt == 'det':
            result = server.detection(img)
        else:
            raise Exception(f"<opt={opt}> is invalid")
        return set_ret(result)
    except Exception as e:
        return set_ret(e)


@app.route('/common/slide-match/<img_type>', methods=['POST'])
def slide_match(img_type='file'):
    try:
        data = request.values

        try:
            method = int(data.get('method', 2))
            target_threshold_min = int(data.get('target_threshold_min', 100))
            target_threshold_max = int(data.get('target_threshold_max', 150))
            background_threshold_min = int(data.get('background_threshold_min', 100))
            background_threshold_max = int(data.get('background_threshold_max', 300))
            border = data.get('border', 'True')
            if border in ['True', 'true', 1]:
                border = True
            else:
                border = False

        except TypeError:
            return {'code': 401, 'results': None, 'msg': '参数错误'}

        target_img = get_img(request, img_type, 'target_img')
        bg_img = get_img(request, img_type, 'bg_img')
        result = server.slide_match(target_img, bg_img, method=method,
                                    target_threshold=(target_threshold_min, target_threshold_max),
                                    background_threshold=(background_threshold_min, background_threshold_max),
                                    border=border)
        return set_ret(result)
    except Exception as e:
        return set_ret(e)


@app.route('/common/slide-compare/<img_type>', methods=['POST'])
def slide_compare(img_type='file'):
    try:
        full_bg_img = get_img(request, img_type, 'full_bg_img')
        bg_img = get_img(request, img_type, 'bg_img')
        result = server.slide_compare(full_bg_img, bg_img)
        return set_ret(result)
    except Exception as e:
        return set_ret(e)


@app.route('/geetest/order-click/<img_type>', methods=['POST'])
def geetest_click(img_type='file'):
    try:
        img = get_img(request, img_type, 'img')
        result = click_in_order(img, ocr=server.ocr_killer, click=server.click_killer)
        return set_ret(result)

    except Exception as e:
        return set_ret(e)


@app.route('/', methods=['GET'])
def index():
    return 'Hello K-Captcha'


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=args.port)
