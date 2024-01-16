"""""""""""""""""""""""""""""
Project: wxtools
Author: Terance Jiang
Date: 1/16/2024
"""""""""""""""""""""""""""""
from typing import Union, List, Tuple, Optional

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
