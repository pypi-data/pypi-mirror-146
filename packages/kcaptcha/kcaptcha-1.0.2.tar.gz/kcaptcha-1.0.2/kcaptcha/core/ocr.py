# --coding:utf-8--
import io
import os
import json

import onnxruntime
import numpy as np
from PIL import Image

from kcaptcha.tools import base64_to_image


class OcrKiller(object):
    def __init__(self, old: bool = False, use_gpu: bool = False, device_id: int = 0):
        self.use_import_onnx = False
        self.__word = False
        self.__resize = []
        self.__channel = 1

        if old:
            self.__graph_path = os.path.join(os.path.dirname(__file__), '../models/common_old.onnx')
            self.__charset = self.__load_charset(old)
        else:
            self.__graph_path = os.path.join(os.path.dirname(__file__), '../models/common.onnx')
            self.__charset = self.__load_charset(old)

        if use_gpu:
            self.__providers = [
                ('CUDAExecutionProvider', {
                    'device_id': device_id,
                    'arena_extend_strategy': 'kNextPowerOfTwo',
                    'cuda_mem_limit': 2 * 1024 * 1024 * 1024,
                    'cudnn_conv_algo_search': 'EXHAUSTIVE',
                    'do_copy_in_default_stream': True,
                }),
            ]
        else:
            self.__providers = [
                'CPUExecutionProvider',
            ]

        self.__ort_session = onnxruntime.InferenceSession(self.__graph_path, providers=self.__providers)

    @classmethod
    def __load_charset(cls, old):
        if old:
            charset_path = os.path.join(os.path.dirname(__file__), '../models/charset_old.json')
        else:
            charset_path = os.path.join(os.path.dirname(__file__), '../models/charset.json')

        with open(charset_path, 'r', encoding='utf-8') as f:
            return json.loads(f.read())

    def classification(self, img_bytes: bytes = None, img_base64: str = None):
        if img_bytes:
            image = Image.open(io.BytesIO(img_bytes))
        else:
            image = base64_to_image(img_base64)

        if not self.use_import_onnx:
            image = image.resize((int(image.size[0] * (64 / image.size[1])), 64), Image.ANTIALIAS).convert('L')

        else:
            if self.__resize[0] == -1:
                if self.__word:
                    image = image.resize((self.__resize[1], self.__resize[1]), Image.ANTIALIAS)
                else:
                    image = image.resize((int(image.size[0] * (self.__resize[1] / image.size[1])), self.__resize[1]),
                                         Image.ANTIALIAS)
            else:
                image = image.resize((self.__resize[0], self.__resize[1]), Image.ANTIALIAS)
            if self.__channel == 1:
                image = image.convert('L')
            else:
                image = image.convert('RGB')
        image = np.array(image).astype(np.float32)
        image = np.expand_dims(image, axis=0) / 255.
        if not self.use_import_onnx:
            image = (image - 0.5) / 0.5
        else:
            if self.__channel == 1:
                image = (image - 0.456) / 0.224
            else:
                image = (image - np.array([0.485, 0.456, 0.406])) / np.array([0.229, 0.224, 0.225])

        ort_inputs = {'input1': np.array([image])}
        ort_outs = self.__ort_session.run(None, ort_inputs)
        result = []

        last_item = 0
        if self.__word:
            for item in ort_outs[1]:
                result.append(self.__charset[item])
        else:
            for item in ort_outs[0][0]:
                if item == last_item:
                    continue
                else:
                    last_item = item
                if item != 0:
                    result.append(self.__charset[item])

        return ''.join(result)


if __name__ == '__main__':
    ocr = OcrKiller()
    pass
