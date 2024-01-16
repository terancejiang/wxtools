"""""""""""""""""""""""""""""
Project: wxtools
Author: Terance Jiang
Date: 1/16/2024
"""""""""""""""""""""""""""""
import numpy as np
import cv2



def draw_bbox(img_draw, bbox, color=(0, 255, 255), thickness=2, xywh=False):
    if xywh:
        bbox[2] += bbox[0]
        bbox[3] += bbox[1]

    cv2.rectangle(img_draw, (int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])),
                  color, thickness)
    return img_draw


def draw_text(img_draw, text, pos, color=(0, 255, 255), thickness=2, font_scale=1):
    cv2.putText(img_draw, text, pos, cv2.FONT_HERSHEY_SIMPLEX, font_scale, color, thickness)
    return img_draw


def draw_landmarks(img_draw, landmarks, color=(0, 255, 255), thickness=2, draw_num=False):

    for idx, landmark in enumerate(landmarks):
        cv2.circle(img_draw, (int(landmark[0]), int(landmark[1])), 2, color, thickness)
        if draw_num:
            draw_text(img_draw, str(idx), (int(landmark[0]), int(landmark[1])), color, thickness)
    return img_draw


def preprocess_2gray(img, size=None):
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
