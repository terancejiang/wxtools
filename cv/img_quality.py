"""""""""""""""""""""""""""""
Project: wxtools
Author: Terance Jiang
Date: 1/16/2024
"""""""""""""""""""""""""""""
import cv2
import numpy as np


def contrast_boost(img: np.ndarray,
                   mode: int) -> np.ndarray:
    """
    Enhance contrast of an image
    :param img:  Input image
    :param mode:  1 or 2
    :return:
    """
    # Mode 1: Enhance contrast using a method involving Gaussian blur and power law transformation
    if mode == 1:
        p = 1.0  # Power for the power law transformation
        ln = img / 255.0  # Normalizing the image values to the range [0, 1]
        G = cv2.GaussianBlur(img, (5, 5), 1.0)  # Applying Gaussian blur to the image
        E = np.power(((G + 0.1) / (img + 0.1)), p)  # Calculating the exponent for power law transformation
        S = np.power(ln, E)  # Applying power law transformation
        res = S * 255.0  # Scaling the result back to the range [0, 255]
        res = res.astype(np.uint8)  # Converting the result to unsigned 8-bit integer format

    # Mode 2: Enhance contrast using median blur and Laplacian operator
    elif mode == 2:
        med = cv2.medianBlur(img, 3)  # Applying median blur to the image
        Lap = cv2.Laplacian(med, -1)  # Applying Laplacian operator to the blurred image
        res = cv2.addWeighted(img, 1, Lap, -0.5, 0)  # Combining the original image and the Laplacian result

    else:
        raise ValueError('Invalid mode')

    return res  # Returning the contrast-enhanced image


def is_bright_zone_large(img: np.ndarray,
                         threshold: float = 0.3,
                         lower: int = 240,
                         higher: int = 255) -> bool:
    """
    Check if the bright area of an image is large
    :param img:     Input image
    :param threshold:  Threshold for the percentage of bright area
    :param lower:  Lower threshold for the intensity of bright pixels
    :param higher:  Higher threshold for the intensity of bright pixels
    :return:  True if the bright area is large, False otherwise
    """
    # Read the image
    # img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    if img is None:
        raise ValueError("Image not found or unable to read.")

    # Find the bright areas; let's consider pixels with intensity > 200 as bright
    _, bright_zones = cv2.threshold(img, lower, higher, cv2.THRESH_BINARY)

    # Calculate the percentage of bright area
    bright_percentage = np.sum(bright_zones == 255) / float(img.size)

    return bright_percentage > threshold


def is_dark_zone_large(img: np.ndarray,
                       threshold: float = 0.2,
                       lower: int = 40,
                       higher: int = 255) -> bool:
    """
    Check if the dark area of an image is large
    :param img:   Input image
    :param threshold:  Threshold for the percentage of dark area
    :param lower:  Lower threshold for the intensity of dark pixels
    :param higher:  Higher threshold for the intensity of dark pixels
    :return:  True if the dark area is large, False otherwise
    """
    # Read the image
    # img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    if img is None:
        raise ValueError("Image not found or unable to read.")

    # Find the bright areas; let's consider pixels with intensity > 200 as bright
    _, dark_zones = cv2.threshold(img, lower, higher, cv2.THRESH_BINARY)

    # Calculate the percentage of bright area
    dark_percentage = np.sum(dark_zones == 0) / float(img.size)

    return dark_percentage > threshold
