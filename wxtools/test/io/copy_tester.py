"""""""""""""""""""""""""""""
Project: wxtools
Author: Terance Jiang
Date: 1/18/2024
"""""""""""""""""""""""""""""
import os
import shutil
import unittest
from unittest import TestCase, mock

from wxtools.io_utils import copy_file_mlpro
from wxtools.logger.utils import colorstr


class TestCopyFileMlpro(TestCase):
    def setUp(self):
        # Create temporary directories for the source and destination
        self.src_root = 'temp_src'
        self.dst_root = 'temp_dst'
        os.makedirs(self.src_root, exist_ok=True)
        os.makedirs(self.dst_root, exist_ok=True)

        # Create a sample file in the source directory
        self.sample_file = 'sample.txt'
        with open(os.path.join(self.src_root, self.sample_file), 'w') as f:
            f.write('This is a test file.')

        # Define file list
        self.file_list = [self.sample_file]

    def tearDown(self):
        # Remove temporary directories after the test
        shutil.rmtree(self.src_root)
        shutil.rmtree(self.dst_root)

    def test_normal_operation(self):
        # Run the copy_file_mlpro function
        copy_file_mlpro(self.file_list, self.src_root, self.dst_root)

        # Check if the file exists in the destination directory
        dst_file_path = os.path.join(self.dst_root, self.sample_file)
        self.assertTrue(os.path.exists(dst_file_path))

        # Check if the file content is preserved
        with open(dst_file_path, 'r') as f:
            content = f.read()
        self.assertEqual(content, 'This is a test file.')

    def test_absent_source_file(self):
        # Remove the source file
        os.remove(os.path.join(self.src_root, self.sample_file))

        with mock.patch('builtins.print') as mock_print:
            copy_file_mlpro(self.file_list, self.src_root, self.dst_root)
            mock_print.assert_called_with(colorstr('red', f'File does not exist: {os.path.join(self.src_root, self.sample_file)}'))

    def test_file_already_exists_in_destination(self):
        # Create a file with the same name in the destination directory
        dst_file_path = os.path.join(self.dst_root, self.sample_file)
        with open(dst_file_path, 'w') as f:
            f.write('Existing file.')

        # Run the copy_file_mlpro function
        copy_file_mlpro(self.file_list, self.src_root, self.dst_root)

        # Check if the file content is not changed
        with open(dst_file_path, 'r') as f:
            content = f.read()
        self.assertEqual(content, 'Existing file.')

    def test_exception_handling(self):
        # Introduce an error in the copying process
        with mock.patch('shutil.copyfile', side_effect=Exception('Mocked exception')):
            with mock.patch('builtins.print') as mock_print:
                copy_file_mlpro(self.file_list, self.src_root, self.dst_root)
                mock_print.assert_called_with(colorstr('red', 'Mocked exception'))

if __name__ == '__main__':
    unittest.main()
