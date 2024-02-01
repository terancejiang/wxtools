"""""""""""""""""""""""""""""
Project: wxtools
Author: Terance Jiang
Date: 1/16/2024
"""""""""""""""""""""""""""""
import os
from typing import Union, List, Tuple, Optional

import onnxruntime as ort
import numpy as np
import cv2


def draw_bbox(img_draw: np.ndarray,
              bbox: Union[List[int], Tuple[int, int, int, int]],
              color: Tuple[int, int, int] = (0, 255, 255),
              thickness: int = 2,
              xywh: bool = False) -> np.ndarray:
    """
    draw bbox on image
    :param img_draw:  image to draw
    :param bbox:  bbox to draw
    :param color:  color of bbox
    :param thickness:  thickness of bbox
    :param xywh:  whether bbox is xywh format
    :return:
    """
    if xywh:
        bbox[2] += bbox[0]
        bbox[3] += bbox[1]

    cv2.rectangle(img_draw, (int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])),
                  color, thickness)
    return img_draw


def draw_text(img_draw: np.ndarray,
              text: str, pos: Tuple[int, int],
              color: Tuple[int, int, int] = (0, 255, 255),
              thickness: int = 2,
              font_scale: float = 1) -> np.ndarray:
    """
    draw text on image
    :param img_draw:  image to draw
    :param text:    text to draw
    :param pos:     position of text
    :param color:   color of text
    :param thickness:   thickness of text
    :param font_scale:  font scale of text
    :return:  image with text
    """
    cv2.putText(img_draw, text, pos, cv2.FONT_HERSHEY_SIMPLEX, font_scale, color, thickness)
    return img_draw


def draw_landmarks(img_draw: np.ndarray,
                   landmarks: List[Tuple[int, int]],
                   color: Tuple[int, int, int] = (0, 255, 255),
                   thickness: int = 2,
                   draw_num: bool = False) -> np.ndarray:
    """
    draw landmarks on image
    :param img_draw:  image to draw
    :param landmarks:  landmarks to draw
    :param color:  color of landmarks
    :param thickness:  thickness of landmarks
    :param draw_num:  whether draw number of landmarks
    :return:  image with landmarks
    """
    for idx, landmark in enumerate(landmarks):
        cv2.circle(img_draw, (int(landmark[0]), int(landmark[1])), 2, color, thickness)
        if draw_num:
            draw_text(img_draw, str(idx), (int(landmark[0]), int(landmark[1])), color, thickness)
    return img_draw


def preprocess_2gray(img: np.ndarray,
                     size: Optional[Tuple[int, int]] = None) -> np.ndarray:
    """
    preprocess image from size (h, w, 3) to (1, 1, h, w)
    :param size: output size
    :param img: cv2 image
    :return: preprocessed image with size (1, 1, h, w)
    """
    if size is not None:
        img = cv2.resize(img, size)

    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    if img.ndim == 2:
        img = img[:, :, np.newaxis]
    img = (img.transpose((2, 0, 1)) - 127.5) * 0.0078125
    img = img.astype(np.float32)
    img = img[np.newaxis, ...]

    return img


def bbox_xywh2xyxy(bbox_xywh: np.ndarray) -> np.ndarray:
    """Transform the bbox format from xywh to x1y1x2y2.

    Args:
        bbox_xywh (ndarray): Bounding boxes (with scores),
            shaped (n, 4) or (n, 5). (left, top, width, height, [score])
    Returns:
        np.ndarray: Bounding boxes (with scores), shaped (n, 4) or
          (n, 5). (left, top, right, bottom, [score])
    """
    bbox_xyxy = bbox_xywh.copy()
    bbox_xyxy[2] = bbox_xyxy[2] + bbox_xyxy[0]
    bbox_xyxy[3] = bbox_xyxy[3] + bbox_xyxy[1]

    return bbox_xyxy


def bbox_xyxy2xywh(bbox_xyxy: np.ndarray) -> np.ndarray:
    """Transform the bbox format from x1y1x2y2to xywh.
    """
    bbox_xywh = bbox_xyxy.copy()
    bbox_xywh[2] = bbox_xywh[2] - bbox_xywh[0]
    bbox_xywh[3] = bbox_xywh[3] - bbox_xywh[1]

    return bbox_xywh


def load_onnx(model_path, cuda=False):
    """
    Load ONNX model.

    Parameters:
    - model_path: path to the ONNX model

    Returns:
    - sess: ONNX model session
    """

    # Load the ONNX model
    if cuda:
        sess = ort.InferenceSession(model_path, providers=['CUDAExecutionProvider'])
    else:
        sess = ort.InferenceSession(model_path, providers=['CPUExecutionProvider'])

    return sess


def rotate_point(pt, rot_mat):
    """
    rotate x,y points by give rotate matrix
    :param pt:
    :param rot_mat:
    :return:
    """
    new_pt = np.array([pt[0], pt[1], 1])
    new_pt = np.dot(rot_mat, new_pt)
    return int(new_pt[0]), int(new_pt[1])


def infer_onnx_model(sess, input_data):
    """
    Load ONNX model and perform inference.

    Parameters:
    - onnx_model_path: path to the ONNX model
    - input_data: numpy array to be input to the model for inference

    Returns:
    - result: output from the model after inference
    """

    # Load the ONNX model
    sess = sess

    # Get input name for the model
    input_name = sess.get_inputs()[0].name

    # Perform inference
    result = sess.run(None, {input_name: input_data})

    return result

