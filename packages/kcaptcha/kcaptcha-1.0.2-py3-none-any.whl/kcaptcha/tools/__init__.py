# --coding:utf-8--
import io
import base64

import cv2
import numpy as np
from PIL import Image


def base64_to_image(img_base64):
    img_data = base64.b64decode(img_base64)
    return Image.open(io.BytesIO(img_data))


def get_img_base64(single_image_path):
    with open(single_image_path, 'rb') as fp:
        img_base64 = base64.b64encode(fp.read())
        return img_base64.decode()


def bytes_to_cv2img(img_bytes):
    img_buffer = np.frombuffer(img_bytes, dtype=np.uint8)
    return cv2.imdecode(img_buffer, 1)


def cv2img_to_bytes(cv2img, suffix='.jpg'):
    _, img_encode = cv2.imencode(suffix, cv2img)
    return img_encode.tobytes()


def pil_to_cv2(pil_img):
    return cv2.cvtColor(np.asarray(pil_img), cv2.COLOR_RGB2BGR)
