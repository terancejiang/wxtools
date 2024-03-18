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
from itertools import groupby
from pathlib import Path
from typing import List, Union, Optional, Tuple, Any

from tqdm import tqdm

from wxtools.logger.utils import colorstr
from wxtools.utils.mlpro_utils import run_mlpro
from wxtools.logger.logger import setup_logger

logger = setup_logger(__name__, log_file=None, log_level='INFO')


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


def restructure_bio_dataset(image_paths: list,
                            dst_root: str,
                            id_index: int, ) -> tuple[list[Any], list[str]]:
    """
    restructure bio dataset, merge images with same id into the same folder, will retrain the same path after id_index
    such as:  ["/path1/[id_index]/x/1.jpg", "/path2/[id_index]/x/2.jpg"] ->
                ["/dst_root/[id_index]/x/1.jpg", "/dst_root/[id_index]/x/2.jpg"]
    :param image_paths:
    :param dst_root:
    :param id_index:
    :return:
    """

    def id_key(x):
        return lambda x: x.split('/')[id_index]

    assert image_paths is not None, "image_paths should not be None"
    assert dst_root is not None, "dst_root should not be None"
    assert id_index is not None, "id_index should not be None"

    assert isinstance(image_paths, list), "image_paths should be a list"

    dst_paths = list()
    src_paths = list()

    image_paths.sort(key=lambda x: x.split('/')[id_index])

    image_groups = groupby(image_paths, key=lambda x: x.split('/')[id_index])
    # image_groups = {k: list(v) for k, v in image_groups}

    for image_id, group in tqdm(image_groups):
        group = list(group)

        dst_dir = os.path.join(dst_root, image_id)
        os.makedirs(dst_dir, exist_ok=True)
        for src_file in group:
            dst_file = os.path.join(dst_dir, "/".join(src_file.split('/')[id_index:]))

            dst_paths.append(dst_file)
            src_paths.append(src_file)

    return src_paths, dst_paths


def replace_root_extension(paths: Union[str, List[str]],
                           src_root: str = None,
                           dst_root: str = None,
                           src_extension: Union[str, List[str]] = None,
                           dst_extension: str = None) -> Union[str, List[str]]:
    """
    replace root and extension
    such as "/src_root/a/b/c.txt" -> "/dst_root/a/b/c.jpg"

    if src_extension and dst_extension are None, then replace root only:
    for example:
    input: ["/src_root/a/b/c.txt",]
    output: ["/dst_root/a/b/c.txt",]

    if src_extension and dst_extension are not None, then replace root and extension,
    extension only will be replaced if the file extension is in given src_extension.
    src_extension can be a list of extensions, such as [".txt", ".png"]
    for example:
    input: "/src_root/a/b/c.txt"
    output: "/dst_root/a/b/c.jpg"
    if src_extension = ".txt" and dst_extension = ".jpg"

    :param dst_extension:
    :param src_extension:
    :param paths:  path or list of paths
    :param src_root:  source root directory
    :param dst_root:  destination root directory
    :return:
    """

    assert all(v is None for v in [src_extension, dst_extension]) or all(
        v is not None for v in [src_extension, dst_extension]), "Either src or dst extensions should be None or all " \
                                                                "should be not None."
    assert (src_root is None and dst_root is None) or (
            src_root is not None and dst_root is not None), "Either src or dst root path should be None or all " \
                                                            "should be not None."

    if isinstance(src_extension, str):
        src_extension = [src_extension]

    if '.' not in dst_extension:
        assert dst_extension is not None, "dst_extension should be a string with a dot, such as '.jpg'"
    if '.' not in src_extension[0]:
        assert src_extension is not None, "src_extension should be a string with a dot, such as '.jpg'"

    if isinstance(paths, str):
        paths = Path(paths)
        if dst_extension is not None:
            paths = replace_suffix(dst_extension, paths, src_extension)

        if src_root is not None:
            sub_path = paths.relative_to(src_root)
            paths = (Path(dst_root) / sub_path).as_posix()

    elif isinstance(paths, list):
        paths = [Path(path) for path in paths]
        if dst_extension is not None:
            paths = [replace_suffix(dst_extension, path, src_extension) for path in paths]

        if src_root is not None:
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


def copy_worker(arg):
    if len(arg) == 2:
        src, dst = arg
        file_path = None
    else:
        src, dst, file_path = arg

    try:
        if file_path is None:
            src_path = src
            dst_path = dst
            if not os.path.exists(src_path):
                logger.info(colorstr('red', 'File does not exist: {}'.format(src_path)))
                return
        else:
            if not os.path.isabs(file_path):
                src_path = os.path.join(src, file_path)
            else:
                src_path = file_path

            if not os.path.exists(src_path):
                logger.info(colorstr('red', 'File does not exist: {}'.format(src_path)))
                return

            dst_path = src_path.replace(src, dst)
            if os.path.exists(dst_path):
                return

        os.makedirs(os.path.dirname(dst_path), exist_ok=True)
        shutil.copyfile(src_path, dst_path)
    except Exception as e:
        logger.info(colorstr('red', e))


def copy_file_mlpro(file_list: Union[str, List[str]] = None,
                    src: Union[str, List[str]] = None,
                    dst: Union[str, List[str]] = None,
                    process_num: int = 10) -> None:
    """
    copy files from src_root to dst_root, with multiprocessing
    :param file_list:  list of file paths, None if src and dst are List of paths
    :param src:  source root directory OR list of source paths
    :param dst:  destination root directory OR list of destination paths
    :param process_num:  number of processes
    :return:  None
    """
    if file_list is not None:
        if isinstance(file_list, str):
            file_list = read_txt(file_list)
        elif isinstance(file_list, list):
            pass

        assert isinstance(src, str) and isinstance(dst, str), \
            "src and dst should be strings when file_list is not None."

        args = [(src, dst, file_path) for file_path in file_list]
    else:
        assert isinstance(src, list) and isinstance(dst, list), \
            "src and dst should be lists when file_list is None."
        assert len(src) == len(dst), \
            "src and dst should have the same length when file_list is None."

        args = list(zip(src, dst))

    run_mlpro(copy_worker, args, process_num)


def get_subdirectories(root: Union[str, Path], level: int, max_level: int) -> List[Path]:
    """
    Get subdirectories from root directory using pathlib.

    :param root: root directory as a Path object
    :param level: current level
    :param max_level: max level
    :return: list of subdirectories as Path objects
    """
    # List to hold subdirectories
    subdirs = []
    root = Path(root) if isinstance(root, str) else root
    # Base case: if the current directory is a directory and we're at or beyond max_level
    if level >= max_level:
        return [root] if root.is_dir() else []

    try:
        # Iterate over the entries in the current directory
        for entry in root.iterdir():
            # Check if the entry is a directory
            if entry.is_dir():
                # Add the subdirectory if the current level is exactly max_level - 1
                if level == max_level - 1:
                    subdirs.append(entry)
                # If we're not at the max_level yet, recurse into the subdirectory
                else:
                    subdirs.extend(get_subdirectories(entry, level + 1, max_level))
    except PermissionError:
        pass  # Ignore directories for which you do not have permission

    return subdirs


def process_directory(arg):
    root, exc, ext = arg
    paths = []
    for dirpath, _, files in os.walk(root):
        file_paths = []
        for x in files:
            x = os.path.join(dirpath, x)
            if exc is not None:
                for e in exc:
                    if e in x:
                        files.remove(x)
                        continue
            if ext is not None:
                if not x.endswith(tuple(ext)):
                    files.remove(x)
                    continue
            file_paths.append(x)
        paths.extend(file_paths)
    return paths


def split_worker(arg: str, separator: str) -> list:
    return arg.split(separator)


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
    # todo change exclude to path, rename extensions

    logger.info(colorstr('green', 'Listing subdirectories from {} to depth {}'.format(root_dir, max_depth)))
    subdirectories = get_subdirectories(root_dir, 0, max_depth)
    logger.info(colorstr('green', 'Found {} subdirectories'.format(len(subdirectories))))

    process_args = [(x, exclude, extensions) for x in subdirectories]

    logger.info(colorstr('green', 'Listing files from {} subdirectories'.format(len(subdirectories))))
    image_paths = run_mlpro(process_directory, process_args, process_num)

    return image_paths
