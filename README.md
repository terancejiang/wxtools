# wxtools

`wxtools` is a comprehensive Python toolkit designed to streamline workflows in image processing, file I/O operations, and similarity computations. 

The Goal of this project is to speed up my own working and research pipelines. Feel free to use or contribute to this project. 

This toolkit is crafted to enhance productivity and efficiency for developers dealing with a wide range of tasks including image enhancements, file management, and analysis of vector similarities.

## Installation

To install `wxtools`, you can clone this repository and install the required dependencies.

```bash
pip install wxtools
```

## Modules
wxtools is composed of three main modules:

`io_utils`: Provides a set of functions for efficient file I/O operations, path manipulations, and batch file processing.
`img_utils`: Offers a collection of image processing utilities to perform tasks such as contrast enhancement, drawing on images, and image transformations.
`similarity`: Includes functions for calculating and analyzing the similarity between vectors, facilitating operations such as cosine similarity computations.
`others`: Other functions that are not included in the above modules.

## Usage
Below are brief examples of how to use each module in wxtools. For detailed usage, refer to the individual function documentation within each module.

### io_utils
```python
from wxtools.io_utils import read_txt, replace_root_extension

# Read text file
lines = read_txt('your_file_path.txt')

# Replace root and extension of a path
new_path = replace_root_extension('/src_root/a/b/c.txt', '/dst_root', src_extension='.txt', dst_extension='.jpg')
```

### img_utils
```python
from wxtools.img_utils import contrast_boost, draw_bbox

# Enhance image contrast
enhanced_img = contrast_boost(image, mode=1)

# Draw bounding box on an image
img_with_bbox = draw_bbox(image, bbox=[x, y, w, h], color=(255, 0, 0), thickness=2, xywh=True)
```

### similarity
```python
from wxtools.similarity import base_cos_sim, feature_cross_sims

# Calculate cosine similarity between two vectors
similarity = base_cos_sim(vector1, vector2)

# Cross calculation of similarity matrix
similar_pairs = feature_cross_sims(matrix_dict, threshold=0.8)
```