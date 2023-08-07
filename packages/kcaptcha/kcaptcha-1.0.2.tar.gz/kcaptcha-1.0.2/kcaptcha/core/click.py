# --coding:utf-8--
import os
import base64

import cv2
import numpy as np
import onnxruntime

from kcaptcha.tools import bytes_to_cv2img


class ClickKiller(object):
    def __init__(self, use_gpu=False, device_id=0):
        self.__graph_path = os.path.join(os.path.dirname(__file__), '../models/common_det.onnx')
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

    def nms(self, boxes, scores, nms_thr):
        """Single class NMS implemented in Numpy."""
        x1 = boxes[:, 0]
        y1 = boxes[:, 1]
        x2 = boxes[:, 2]
        y2 = boxes[:, 3]

        areas = (x2 - x1 + 1) * (y2 - y1 + 1)
        order = scores.argsort()[::-1]

        keep = []
        while order.size > 0:
            i = order[0]
            keep.append(i)
            xx1 = np.maximum(x1[i], x1[order[1:]])
            yy1 = np.maximum(y1[i], y1[order[1:]])
            xx2 = np.minimum(x2[i], x2[order[1:]])
            yy2 = np.minimum(y2[i], y2[order[1:]])

            w = np.maximum(0.0, xx2 - xx1 + 1)
            h = np.maximum(0.0, yy2 - yy1 + 1)
            inter = w * h
            ovr = inter / (areas[i] + areas[order[1:]] - inter)

            inds = np.where(ovr <= nms_thr)[0]
            order = order[inds + 1]

        return keep

    def multiclass_nms_class_agnostic(self, boxes, scores, nms_thr, score_thr):
        """Multiclass NMS implemented in Numpy. Class-agnostic version."""
        cls_inds = scores.argmax(1)
        cls_scores = scores[np.arange(len(cls_inds)), cls_inds]

        valid_score_mask = cls_scores > score_thr
        if valid_score_mask.sum() == 0:
            return None
        valid_scores = cls_scores[valid_score_mask]
        valid_boxes = boxes[valid_score_mask]
        valid_cls_inds = cls_inds[valid_score_mask]
        keep = self.nms(valid_boxes, valid_scores, nms_thr)
        dets = None
        if keep:
            dets = np.concatenate(
                [valid_boxes[keep], valid_scores[keep, None], valid_cls_inds[keep, None]], 1
            )
        return dets

    def multiclass_nms(self, boxes, scores, nms_thr, score_thr):
        """Multiclass NMS implemented in Numpy"""
        return self.multiclass_nms_class_agnostic(boxes, scores, nms_thr, score_thr)

    def demo_postprocess(self, outputs, img_size, p6=False):
        grids = []
        expanded_strides = []

        if not p6:
            strides = [8, 16, 32]
        else:
            strides = [8, 16, 32, 64]

        hsizes = [img_size[0] // stride for stride in strides]
        wsizes = [img_size[1] // stride for stride in strides]

        for hsize, wsize, stride in zip(hsizes, wsizes, strides):
            xv, yv = np.meshgrid(np.arange(wsize), np.arange(hsize))
            grid = np.stack((xv, yv), 2).reshape(1, -1, 2)
            grids.append(grid)
            shape = grid.shape[:2]
            expanded_strides.append(np.full((*shape, 1), stride))

        grids = np.concatenate(grids, 1)
        expanded_strides = np.concatenate(expanded_strides, 1)
        outputs[..., :2] = (outputs[..., :2] + grids) * expanded_strides
        outputs[..., 2:4] = np.exp(outputs[..., 2:4]) * expanded_strides

        return outputs

    def preproc(self, img, input_size, swap=(2, 0, 1)):
        if len(img.shape) == 3:
            padded_img = np.ones((input_size[0], input_size[1], 3), dtype=np.uint8) * 114
        else:
            padded_img = np.ones(input_size, dtype=np.uint8) * 114

        r = min(input_size[0] / img.shape[0], input_size[1] / img.shape[1])
        resized_img = cv2.resize(
            img,
            (int(img.shape[1] * r), int(img.shape[0] * r)),
            interpolation=cv2.INTER_LINEAR,
        )

        padded_img[: int(img.shape[0] * r), : int(img.shape[1] * r)] = resized_img.astype(np.uint8)

        # 转置
        padded_img = padded_img.transpose(swap)
        padded_img = np.ascontiguousarray(padded_img, dtype=np.float32)

        return padded_img, r

    def get_bbox(self, image_bytes):
        img = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)

        im, ratio = self.preproc(img, (416, 416))

        ort_inputs = {self.__ort_session.get_inputs()[0].name: im[None, :, :, :]}

        output = self.__ort_session.run(None, ort_inputs)

        predictions = self.demo_postprocess(output[0], (416, 416))[0]
        boxes = predictions[:, :4]
        scores = predictions[:, 4:5] * predictions[:, 5:]

        boxes_xyxy = np.ones_like(boxes)
        boxes_xyxy[:, 0] = boxes[:, 0] - boxes[:, 2] / 2.
        boxes_xyxy[:, 1] = boxes[:, 1] - boxes[:, 3] / 2.
        boxes_xyxy[:, 2] = boxes[:, 0] + boxes[:, 2] / 2.
        boxes_xyxy[:, 3] = boxes[:, 1] + boxes[:, 3] / 2.
        boxes_xyxy /= ratio

        pred = self.multiclass_nms(boxes_xyxy, scores, nms_thr=0.45, score_thr=0.1)

        try:
            temp = pred[:, :4]
            final_boxes = temp.tolist()
            result = []
            for b in final_boxes:
                if b[0] < 0:
                    x_min = 0
                else:
                    x_min = int(b[0])
                if b[1] < 0:
                    y_min = 0
                else:
                    y_min = int(b[1])
                if b[2] > img.shape[1]:
                    x_max = int(img.shape[1])
                else:
                    x_max = int(b[2])
                if b[3] > img.shape[0]:
                    y_max = int(img.shape[0])
                else:
                    y_max = int(b[3])
                result.append([x_min, y_min, x_max, y_max])
        except Exception as e:
            return []
        return result

    def detection(self, img_bytes: bytes = None, img_base64: str = None, debug: bool = False):

        if not img_bytes:
            img_bytes = base64.b64decode(img_base64)
        result = self.get_bbox(img_bytes)

        if debug:
            img = bytes_to_cv2img(img_bytes)
            for each in result:
                img = cv2.rectangle(img, (each[0], each[1]), (each[2], each[3]), thickness=2, color=(0, 0, 255))
                cv2.imshow('Result', img)
                cv2.waitKey()

        return result


def test():
    click_killer = ClickKiller()
    with open('../imgs/common_click_1.png', 'rb') as f:
        img_bytes = f.read()

    result = click_killer.detection(img_bytes, debug=True)
    print(result)


if __name__ == '__main__':
    test()
    pass
