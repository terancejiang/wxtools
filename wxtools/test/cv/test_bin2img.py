#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Name: wxtools
File Created: 2024/2/1 下午5:14
Author: Ying.Jiang
File Name: test_bin2img.py
"""
import numpy as np
import os
import cv2
from typing import Union, List, Tuple
from unittest import TestCase, main

from wxtools.cv.bin2png import bin2img


class TestBin2Img(TestCase):

    def setUp(self):
        # Setup for the tests, like creating dummy files, etc.
        self.valid_image_path = "test.bin"
        self.invalid_image_path = "test.txt"
        self.valid_image = np.random.randint(0, 256, (600, 800), dtype=np.uint8)
        self.invalid_image = np.random.randint(0, 256, (300, 400), dtype=np.uint8)
        np.array(self.valid_image, dtype=np.uint8).tofile(self.valid_image_path)

    def tearDown(self):
        # Clean up after tests, like deleting dummy files
        if os.path.exists(self.valid_image_path):
            os.remove(self.valid_image_path)

    def test_single_image_path(self):
        # Test with a single valid image path
        result = bin2img(self.valid_image_path)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)

    def test_single_image_path_invalid(self):
        # Test with a single invalid image path
        with self.assertRaises(ValueError):
            bin2img(self.invalid_image_path)

    def test_list_of_image_paths(self):
        # Test with a list of valid image paths
        result = bin2img([self.valid_image_path, self.valid_image_path])
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)

    def test_list_of_image_paths_invalid(self):
        # Test with a list of invalid image paths
        with self.assertRaises(ValueError):
            bin2img([self.invalid_image_path])

    def test_single_binary_image(self):
        # Test with a single binary image
        result = bin2img(self.valid_image)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)

    def test_single_binary_image_invalid(self):
        # Test with a single invalid binary image
        with self.assertRaises(ValueError):
            bin2img(self.invalid_image)

    def test_list_of_binary_images(self):
        # Test with a list of binary images
        result = bin2img([self.valid_image, self.valid_image])
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)

    def test_list_of_binary_images_invalid(self):
        # Test with a list of invalid binary images
        with self.assertRaises(ValueError):
            bin2img([self.invalid_image])

    def test_output_dst(self):
        # Test with output_dst parameter
        output_dst = "output"
        os.makedirs(output_dst, exist_ok=True)
        bin2img([self.valid_image_path], output_dst=output_dst)
        output_files = os.listdir(output_dst)
        self.assertEqual(len(output_files), 1)
        # Clean up
        for file in output_files:
            os.remove(os.path.join(output_dst, file))
        os.rmdir(output_dst)

    def test_incorrect_size(self):
        # Test with incorrect size parameter
        with self.assertRaises(ValueError):
            bin2img(self.valid_image_path, size=(100, 100))


if __name__ == "__main__":
    main()
