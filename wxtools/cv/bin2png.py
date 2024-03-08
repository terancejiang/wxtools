#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Name: wxtools
File Created: 2024/2/1 下午5:31
Author: Ying.Jiang
File Name: bin2png.py
"""
import argparse
import os
import tkinter as tk
from tkinter import filedialog, font

import cv2
import numpy as np


# def bin2img(images: Union[np.ndarray, str, List[np.ndarray], List[str]],
#             img_size: Tuple[int, int] = (600, 800),
#             channel: int = 1,
#             output_dst: str = None) -> List[np.ndarray]:
def bin2img(images, img_size=(600, 800), channel=1, output_dst=None):
    """
    convert binary image to cv2 images
    :param channel:  channel of binary image
    :param output_dst:  output directory
    :param images: can be 1. a image path, 2. a single binary image, 3. list of paths, 4. list of binary images
    :param img_size: binary image size in (width, height), default is (600, 800)
    :return: cv2 image or list of cv2 images
    """
    image_paths = []
    # image is a single image path, or a directory
    if isinstance(images, str):
        if os.path.isdir(images):
            image_paths = [os.path.join(images, image) for image in os.listdir(images)]
            image_paths = [image for image in image_paths if image.endswith(".bin")]
            images = [np.fromfile(image, dtype=np.uint8) for image in image_paths]
        elif os.path.exists(images):
            if not os.path.exists(images):
                raise ValueError("image path does not exist")
            if not images.endswith(".bin"):
                raise ValueError("image path should be a binary image")
            image_paths = [images]
            images = [np.fromfile(images, dtype=np.uint8)]
        else:
            raise ValueError("image path does not exist")
    # image is a single image
    elif isinstance(images, np.ndarray):
        images = [images]
    elif isinstance(images, list):
        # image is a list of image paths
        if isinstance(images[0], str):
            if not all([os.path.exists(image) for image in images]):
                raise ValueError("image path does not exist")
            if not all([image.endswith(".bin") for image in images]):
                raise ValueError("image path should be a binary image")
            image_paths = images
            images = [np.fromfile(image, dtype=np.uint8) for image in images]
        # image is a list of images
        else:
            images = images
    else:
        raise ValueError("images should be str, np.ndarray or list")

    width, height = img_size
    channel = channel
    converted_images = []
    for idx, image in enumerate(images):
        image = image[0:width * height]

        image_output = np.reshape(image, (height, width, channel))
        converted_images.append(image_output)

        if output_dst is not None:
            if len(image_paths) > 0:
                output_path = os.path.join(output_dst, os.path.basename(image_paths[idx]).replace(".bin", ".png"))
            else:
                output_path = os.path.join(output_dst, f"image_{idx}.png")
            if not os.path.exists(output_dst):
                os.makedirs(output_dst, exist_ok=True)
            cv2.imwrite(output_path, image_output)

    return converted_images


class Bin2ImgApp:
    def __init__(self, master):
        self.master = master
        master.title("Bin2Img Converter")

        # Define a larger font
        self.custom_font = font.Font(family="Helvetica", size=20)

        # Apply the font to labels, entries, and buttons
        tk.Label(master, text="Source Folder:", font=self.custom_font).grid(row=0)
        tk.Label(master, text="Output Folder:", font=self.custom_font).grid(row=1)
        tk.Label(master, text="Image Size (WxH):", font=self.custom_font).grid(row=2)
        tk.Label(master, text="Channel:", font=self.custom_font).grid(row=3)

        self.src_entry = tk.Entry(master, font=self.custom_font)
        self.src_entry.grid(row=0, column=1)
        tk.Button(master, text="Browse", font=self.custom_font, command=self.browse_src).grid(row=0, column=2)

        self.out_entry = tk.Entry(master, font=self.custom_font)
        self.out_entry.grid(row=1, column=1)
        tk.Button(master, text="Browse", font=self.custom_font, command=self.browse_out).grid(row=1, column=2)

        self.size_entry = tk.Entry(master, font=self.custom_font)
        self.size_entry.insert(0, "600x800")  # Default size
        self.size_entry.grid(row=2, column=1)

        self.channel_entry = tk.Entry(master, font=self.custom_font)
        self.channel_entry.insert(0, "1")  # Default channel
        self.channel_entry.grid(row=3, column=1)

        tk.Button(master, text="Convert", font=self.custom_font, command=self.convert).grid(row=4, column=1)

    def browse_src(self):
        directory = filedialog.askdirectory()
        self.src_entry.delete(0, tk.END)
        self.src_entry.insert(0, directory)

    def browse_out(self):
        directory = filedialog.askdirectory()
        self.out_entry.delete(0, tk.END)
        self.out_entry.insert(0, directory)

    def convert(self):
        # Conversion logic remains the same
        src_dir = self.src_entry.get()
        out_dir = self.out_entry.get()
        size = tuple(map(int, self.size_entry.get().split('x')))
        channel = int(self.channel_entry.get())

        images = src_dir  # Pass the source directory directly
        bin2img(images, img_size=size, channel=channel, output_dst=out_dir)
        CustomDialog(self.master, "Images converted successfully.")


class CustomDialog:
    def __init__(self, master, text):
        top = self.top = tk.Toplevel(master)
        self.custom_font = font.Font(family="Helvetica", size=12)  # Custom font

        tk.Label(top, text=text, font=self.custom_font).pack(pady=10)
        tk.Button(top, text="OK", command=self.ok, font=self.custom_font).pack(pady=5)

    def ok(self):
        self.top.destroy()

# if __name__ == "__main__":
#     root = tk.Tk()
#     app = Bin2ImgApp(root)
#     root.mainloop()
# # #
if __name__ == "__main__":

    # Example usage:
    # python bin2img.py --images /image/path --size 600 800 --channel 1 --output_dst /output/directory

    parser = argparse.ArgumentParser(description='Convert binary image(s) to cv2 images.')
    parser.add_argument('--images', nargs='+', default='',
                        help='Path to the image(s). Can be a single image path, or multiple image paths')
    parser.add_argument('--size', nargs=2, type=int, default=[600, 800],
                        help='Size of the output images as two integers: width height')
    parser.add_argument('--channel', type=int, default=1, help='Number of channels in the image')
    parser.add_argument('--output_dst', type=str, help='Output directory to save the images')

    args = parser.parse_args()

    # Convert the size argument from list to tuple
    size = tuple(args.size)

    # Call the bin2img function with the parsed arguments
    converted_images = bin2img(images=args.images, img_size=size, channel=args.channel, output_dst=args.output_dst)

    print("Images converted successfully.")
