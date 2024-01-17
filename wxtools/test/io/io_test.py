"""""""""""""""""""""""""""""
Project: wxtools
Author: Terance Jiang
Date: 1/17/2024
"""""""""""""""""""""""""""""

from wxtools.io_utils import replace_root_extension

def test_1():
    # test replace_root_extension
    # replace root only
    print(replace_root_extension(r"C:\Users\jiang\PycharmProjects\wxtools\test\io\test.txt",
                                 r"C:\Users\jiang\PycharmProjects\wxtools\test\io",
                                 r"C:\Users\jiang\PycharmProjects\wxtools\test\io\test2"))

    print(replace_root_extension(r"C:\Users\jiang\PycharmProjects\wxtools\test\io\test.txt",
                                 r"C:\Users\jiang\PycharmProjects\wxtools\test\io",
                                 r"C:\Users\jiang\PycharmProjects\wxtools\test\io\test2",
                                 src_extension=".txt",
                                 dst_extension=".jpg"))
    print(replace_root_extension([r"C:\Users\jiang\PycharmProjects\wxtools\test\io\testc.txt",
                                  r"C:\Users\jiang\PycharmProjects\wxtools\test\io\testy.png",
                                  r"C:\Users\jiang\PycharmProjects\wxtools\test\io\testx.jpg"],
                                 r"C:\Users\jiang\PycharmProjects\wxtools\test\io",
                                 r"C:\Users\jiang\PycharmProjects\wxtools\test\io\test2",
                                 src_extension=[".txt", ".png"],
                                 dst_extension=".xyz"))


if __name__ == '__main__':
    test_1()