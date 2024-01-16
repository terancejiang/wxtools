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

from tqdm import tqdm

from logger.utils import colorstr

def read_txt(file_path):
    if not os.path.exists(file_path):
        raise ValueError('File path does not exist')
    if not file_path.endswith('.txt'):
        raise ValueError('File path must end with .txt')

    with open(file_path, 'r') as file:
        raw_data = file.readlines()
    raw_data = [line.strip() for line in raw_data]
    return raw_data


def read_str_format_list(file_path):
    if not file_path.endswith('.txt'):
        raise ValueError('File path must end with .txt')
    if not os.path.exists(file_path):
        raise ValueError('File path does not exist')

    with open(file_path, 'r') as file:
        raw_data = file.read()
        return ast.literal_eval(raw_data)


def read_json_object(file_path):
    if not file_path.endswith('.json'):
        raise ValueError('File path must end with .json')
    if not os.path.exists(file_path):
        raise ValueError('File path does not exist')

    # read json object
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data


def find_subfolders_with_string(root_dir, search_string):
    matching_folders = []
    for root, dirs, files in os.walk(root_dir):
        for dir in dirs:
            if search_string in dir:
                matching_folders.append(os.path.join(root, dir))

    return matching_folders


def copy_file_mlpro(file_list, src_root, dst_root, process_num):
    def copy(arg):
        src, dst, file_path = arg
        try:
            if not os.path.isabs(file_path):
                src_path = os.path.join(src, file_path)
            else:
                src_path = file_path

            if not os.path.exists(src):
                print(colorstr('red','File does not exist: {}'.format(src_path)))
                return

            dst_path = src_path.replace(src, dst)
            if os.path.exists(dst_path):
                return

            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copyfile(src, dst)
        except Exception as e:
            print(colorstr('red',e))

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


def get_subdirectories(root, level, max_level):
    """ Recursively get subdirectories up to a specified level. """
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


def list_files_mlpro(root_dir, process_num, max_depth=1, exclude=None, extensions=None):
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
