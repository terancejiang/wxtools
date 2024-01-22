## API Documentation for `io_utils.py`

### 1. `replace_root_extension(paths, src_root, dst_root, src_extension, dst_extension)`
Replaces the root directory and the file extension of the given paths. If `src_extension` and `dst_extension` are provided, it replaces the file extension only if it matches `src_extension`. `src_extension` can be a single extension or a list of extensions.

- **Parameters**:
  - `paths` (Union[str, List[str]]): Path or list of paths to modify.
  - `src_root` (str): Source root directory.
  - `dst_root` (str): Destination root directory.
  - `src_extension` (Optional[Union[str, List[str]]]): Source file extension(s) to match for replacement.
  - `dst_extension` (Optional[str]): Destination file extension for replacement.
- **Returns**: None. Performs the replacement operation in-place.

---

### 2. `read_txt(file_path)`
Reads a text file and returns its contents as a list of lines.

- **Parameters**:
  - `file_path` (str): Path of the text file to read.
- **Returns**:
  - `List[str]`: List of lines read from the text file.

---

### 3. `read_str_format_list(file_path)`
Reads a text file with a specific string format and returns its contents as a list of lines.

- **Parameters**:
  - `file_path` (str): Path of the text file to read.
- **Returns**:
  - `List[str]`: List of lines read from the text file.

---

### 4. `read_json_object(file_path)`
Reads a JSON object from a file.

- **Parameters**:
  - `file_path` (str): Path of the JSON file to read.
- **Returns**:
  - `dict`: JSON object read from the file.

---

### 5. `find_subfolders_with_string(root_dir, search_string)`
Finds and returns a list of subfolders within the `root_dir` that contain the `search_string`.

- **Parameters**:
  - `root_dir` (str): Root directory to search within.
  - `search_string` (str): String to search for in subfolder names.
- **Returns**:
  - `List[str]`: List of subfolders that contain the search string.

---

### 6. `copy_file_mlpro(file_list, src, dst, process_num)`
Copies files from the source to the destination using multiprocessing. If `file_list` is provided, it copies specific files. Otherwise, it treats `src` and `dst` as lists of paths.

- **Parameters**:
  - `file_list` (Optional[List[str]]): List of file paths to copy.
  - `src` (Union[str, List[str]]): Source directory or list of source paths.
  - `dst` (Union[str, List[str]]): Destination directory or list of destination paths.
  - `process_num` (int): Number of processes to use for copying.
- **Returns**: None. Performs the copy operation.

---

### 7. `get_subdirectories(root, level, max_level)`
Gets subdirectories from the `root` directory up to a specified `max_level` of depth.

- **Parameters**:
  - `root` (Path): Root directory as a Path object.
  - `level` (int): Current level (usually start with 0 or 1).
  - `max_level` (int): Maximum depth level to search for subdirectories.
- **Returns**:
  - `List[Path]`: List of subdirectories as Path objects.

---

### 8. `list_files_mlpro(root_dir, process_num, max_depth, exclude, extensions)`
Lists files in the `root_dir` using multiprocessing, optionally filtering by `max_depth`, `exclude` list, and file `extensions`.

- **Parameters**:
  - `root_dir` (str): Root directory to list files from.
  - `process_num` (int): Number of processes to use for listing.
  - `max_depth` (int): Maximum depth to search for files.
  - `exclude` (Optional[List[str]]): List of strings to exclude from the search.
  - `extensions` (Optional[List[str]]): List of file extensions to include in the search.
- **Returns**:
  - `List[str]`: List of file paths that match the criteria.

---

### 9. `replace_suffix(dst_extension, path, allowed_extensions)`
Replaces the suffix of the given `path` with `dst_extension`, if the current suffix is in the list of `allowed_extensions`.

- **Parameters**:
  - `dst_extension` (str): Destination file extension for the replacement.
  - `path` (str): File path for which the suffix is to be replaced.
  - `allowed_extensions` (Optional[List[str]]): List of allowed extensions for replacement.
- **Returns**:
  - `str`: Path with the replaced suffix.

---

