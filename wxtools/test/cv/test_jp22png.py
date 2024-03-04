import unittest
import os
from PIL import Image
import numpy as np

from wxtools.cv.img_utils import convert_jp2_to_image


class TestConvertJP2ToImage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create a temporary JP2 image for testing
        cls.temp_dir = "temp_test_dir"
        cls.output_dir = "output_test_dir"
        os.makedirs(cls.temp_dir, exist_ok=True)
        os.makedirs(cls.output_dir, exist_ok=True)

        # Create a dummy image and save as JP2
        cls.test_image_name = "test_image.jp2"
        cls.test_image_path = os.path.join(cls.temp_dir, cls.test_image_name)
        image = Image.fromarray(np.zeros((100, 100, 3), dtype=np.uint8))
        image.save(cls.test_image_path)

    @classmethod
    def tearDownClass(cls):
        # Remove temporary files and directories after tests
        os.remove(cls.test_image_path)
        os.rmdir(cls.temp_dir)
        for filename in os.listdir(cls.output_dir):
            os.remove(os.path.join(cls.output_dir, filename))
        os.rmdir(cls.output_dir)

    def test_single_jp2_to_jpg_conversion(self):
        # Test conversion of a single JP2 image to JPG format
        convert_jp2_to_image(self.test_image_path, self.output_dir, 'jpg')

        expected_output_path = os.path.join(self.output_dir, "test_image.jpg")
        self.assertTrue(os.path.exists(expected_output_path), "Output JPG file does not exist.")

        # Optionally, check if the output image can be opened, implying correct format
        with Image.open(expected_output_path) as img:
            self.assertEqual(img.format, 'JPEG', "Output image is not in JPG format.")


# Run the test
if __name__ == '__main__':
    unittest.main()
