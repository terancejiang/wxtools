"""""""""""""""""""""""""""""
Project: wxtools
Author: Terance Jiang
Date: 1/16/2024
"""""""""""""""""""""""""""""
import ast
import json
import multiprocessing
import os
import shutil
from pathlib import Path
from typing import List, Union, Optional

from tqdm import tqdm

from wxtools.logger.utils import colorstr


def replace_root_extension(paths: Union[str, List[str]],
                           src_root: str,
                           dst_root: str,
                           src_extension: Union[str, List[str]] = None,
                           dst_extension: str = None) -> Union[str, List[str]]:
    """
    replace root and extension
    such as "/src_root/a/b/c.txt" -> "/dst_root/a/b/c.jpg"

    if src_extension and dst_extension are None, then replace root only

    if src_extension and dst_extension are not None, then replace root and extension,
    extension only will be replaced if the file extension is in given src_extension.
    such as "/src_root/a/b/c.txt" -> "/dst_root/a/b/c.jpg" if src_extension = ".txt" and dst_extension = ".jpg"
    src_extension can be a list of extensions, such as [".txt", ".png"]

    :param dst_extension:
    :param src_extension:
    :param paths:  path or list of paths
    :param src_root:  source root directory
    :param dst_root:  destination root directory
    :return:
    """

    def replace_suffix(dst_extension: str, path: Path, allowed_extensions: List[str] = None):
        """
        replace suffix of a path
        :param dst_extension:
        :param path:
        :param allowed_extensions:
        :return:  path with replaced suffix
        """
        if dst_extension is not None:
            if path.suffix in allowed_extensions:
                path = path.with_suffix(dst_extension)
        return path

    assert all(v is None for v in [src_extension, dst_extension]) or all(
        v is not None for v in [src_extension, dst_extension]), "Either src or dst extensions should be None or all " \
                                                                "should be not None."
    if isinstance(src_extension, str):
        src_extension = [src_extension]

    if isinstance(paths, str):
        paths = Path(paths)
        if dst_extension is not None:
            paths = replace_suffix(dst_extension, paths, src_extension)

        sub_path = paths.relative_to(src_root)
        paths = (Path(dst_root) / sub_path).as_posix()

    elif isinstance(paths, list):
        paths = [Path(path) for path in paths]
        if dst_extension is not None:
            paths = [replace_suffix(dst_extension, path, src_extension) for path in paths]

        paths = [(Path(dst_root) / path.relative_to(src_root)).as_posix() for path in paths]

    return paths


def read_txt(file_path: str) -> List[str]:
    """
    read txt file
    :param file_path:  path of txt file
    :return:  list of lines
    """
    if not os.path.exists(file_path):
        raise ValueError('File path does not exist')
    if not file_path.endswith('.txt'):
        raise ValueError('File path must end with .txt')

    with open(file_path, 'r') as file:
        raw_data = file.readlines()
    raw_data = [line.strip() for line in raw_data]
    return raw_data


def read_str_format_list(file_path: str) -> List[str]:
    """
    read txt file with str format
    :param file_path:  path of txt file
    :return:  list of lines
    """
    if not file_path.endswith('.txt'):
        raise ValueError('File path must end with .txt')
    if not os.path.exists(file_path):
        raise ValueError('File path does not exist')

    with open(file_path, 'r') as file:
        raw_data = file.read()
        return ast.literal_eval(raw_data)


def read_json_object(file_path: str) -> dict:
    """
    read json object
    :param file_path:  path of json file
    :return:  json object
    """
    if not file_path.endswith('.json'):
        raise ValueError('File path must end with .json')
    if not os.path.exists(file_path):
        raise ValueError('File path does not exist')

    # read json object
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data


def find_subfolders_with_string(root_dir: str,
                                search_string: str) -> List[str]:
    """
    find subfolders with string in root directory
    :param root_dir:  root directory
    :param search_string:  string to search
    :return:  list of subfolders
    """
    matching_folders = []
    for root, dirs, files in os.walk(root_dir):
        for dir in dirs:
            if search_string in dir:
                matching_folders.append(os.path.join(root, dir))

    return matching_folders


def copy_file_mlpro(file_list: Union[str, List[str]],
                    src_root: str,
                    dst_root: str,
                    process_num: int) -> None:
    """
    copy files from src_root to dst_root, with multiprocessing
    :param file_list:  list of file paths
    :param src_root:  source root directory
    :param dst_root:  destination root directory
    :param process_num:  number of processes
    :return:  None
    """

    def copy(arg):
        src, dst, file_path = arg
        try:
            if not os.path.isabs(file_path):
                src_path = os.path.join(src, file_path)
            else:
                src_path = file_path

            if not os.path.exists(src):
                print(colorstr('red', 'File does not exist: {}'.format(src_path)))
                return

            dst_path = src_path.replace(src, dst)
            if os.path.exists(dst_path):
                return

            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copyfile(src, dst)
        except Exception as e:
            print(colorstr('red', e))

    if isinstance(file_list, str):
        file_list = read_txt(file_list)
    elif isinstance(file_list, list):
        pass

    args = [(src_root, dst_root, file_path) for file_path in file_list]

    pool = multiprocessing.Pool(process_num)

    for _ in tqdm(pool.imap_unordered(copy, args), total=len(args)):
        pass

    pool.close()
    pool.join()


def get_subdirectories(root: str,
                       level: int,
                       max_level: int) -> List[str]:
    """
    get subdirectories from root directory
    :param root:  root directory
    :param level:  current level
    :param max_level:   max level
    :return:  list of subdirectories
    """
    if level >= max_level:
        return [root]
    subdirs = []
    try:
        for entry in os.listdir(root):
            path = os.path.join(root, entry)
            if os.path.isdir(path):
                subdirs.extend(get_subdirectories(path, level + 1, max_level))
    except PermissionError:
        pass  # Ignore directories for which you do not have permission
    return subdirs


def list_files_mlpro(root_dir: str,
                     process_num: int,
                     max_depth: int = 1,
                     exclude: Optional[List[str]] = None,
                     extensions: Optional[List[str]] = None) -> List[str]:
    """
    list files with multiprocessing
    :param root_dir:  root directory
    :param process_num:  number of processes
    :param max_depth:  max depth
    :param exclude:  list of strings to exclude
    :param extensions:  list of extensions
    :return:  list of file paths
    """

    def process_directory(root, exc, ext):
        paths = []
        for dirpath, _, files in os.walk(root):
            file_paths = []
            for x in files:
                if exc is not None:
                    for e in exc:
                        if e in x:
                            files.remove(x)
                            continue
                if ext is not None:
                    if not x.endswith(tuple(ext)):
                        files.remove(x)
                        continue
                file_paths.append(os.path.join(dirpath, x))
            paths.extend(file_paths)
        return paths

    pool = multiprocessing.Pool(processes=process_num)

    print(colorstr('green', 'Listing subdirectories from {} to depth {}'.format(root_dir, max_depth)))
    subdirectories = get_subdirectories(root_dir, 0, max_depth)
    print(colorstr('green', 'Found {} subdirectories'.format(len(subdirectories))))

    process_args = [(x, exclude, extensions) for x in subdirectories]

    print(colorstr('green', 'Listing files from {} subdirectories'.format(len(subdirectories))))
    image_paths = []
    for _ in tqdm(pool.imap_unordered(process_directory, process_args), total=len(process_args)):
        image_paths.extend(_)

    pool.close()
    pool.join()

    return image_paths
