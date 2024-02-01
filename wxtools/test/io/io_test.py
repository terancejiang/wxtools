"""""""""""""""""""""""""""""
Project: wxtools
Author: Terance Jiang
Date: 1/17/2024
"""""""""""""""""""""""""""""

import os
import unittest
import tempfile

from wxtools.io_utils.io_utils import list_files_mlpro
from wxtools.io_utils import replace_root_extension


class TestListFilesMlpro(unittest.TestCase):
    def setUp(self):
        # Set up a temporary directory with known structure
        self.root_dir = tempfile.mkdtemp()

        # Create subdirectories and files
        os.makedirs(os.path.join(self.root_dir, 'dir1'), exist_ok=True)
        os.makedirs(os.path.join(self.root_dir, 'dir2'), exist_ok=True)
        self.known_files = ['file1.txt', 'file2.py', 'file3.txt']
        for file in self.known_files:
            with open(os.path.join(self.root_dir, 'dir1', file), 'w') as f:
                f.write('test')
            with open(os.path.join(self.root_dir, 'dir2', file), 'w') as f:
                f.write('test')

    def tearDown(self):
        # Clean up the directory after the test
        for root, dirs, files in os.walk(self.root_dir, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(self.root_dir)

    def test_list_files_mlpro(self):
        # Call the function
        result_paths = list_files_mlpro(self.root_dir, process_num=2, max_depth=1)

        # Generate the expected result
        expected_paths = [os.path.join(self.root_dir, 'dir1', file) for file in self.known_files]
        expected_paths += [os.path.join(self.root_dir, 'dir2', file) for file in self.known_files]

        # Check if the results are as expected
        self.assertCountEqual(result_paths, expected_paths)


# def test_1():
#     # test replace_root_extension
#     # replace root only
#     logger.info(replace_root_extension(r"C:\Users\jiang\PycharmProjects\wxtools\test\io\test.txt",
#                                  r"C:\Users\jiang\PycharmProjects\wxtools\test\io",
#                                  r"C:\Users\jiang\PycharmProjects\wxtools\test\io\test2"))
#
#     logger.info(replace_root_extension(r"C:\Users\jiang\PycharmProjects\wxtools\test\io\test.txt",
#                                  r"C:\Users\jiang\PycharmProjects\wxtools\test\io",
#                                  r"C:\Users\jiang\PycharmProjects\wxtools\test\io\test2",
#                                  src_extension=".txt",
#                                  dst_extension=".jpg"))
#     logger.info(replace_root_extension([r"C:\Users\jiang\PycharmProjects\wxtools\test\io\testc.txt",
#                                   r"C:\Users\jiang\PycharmProjects\wxtools\test\io\testy.png",
#                                   r"C:\Users\jiang\PycharmProjects\wxtools\test\io\testx.jpg"],
#                                  r"C:\Users\jiang\PycharmProjects\wxtools\test\io",
#                                  r"C:\Users\jiang\PycharmProjects\wxtools\test\io\test2",
#                                  src_extension=[".txt", ".png"],
#                                  dst_extension=".xyz"))


if __name__ == '__main__':
    # test_1()
    unittest.main()