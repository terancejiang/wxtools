## API Documentation for `cv`

### 1. `contrast_boost(img, mode)`
Enhances the contrast of an image.
- **Parameters**:
  - `img` (np.ndarray): Input image.
  - `mode` (int): Mode of contrast enhancement (1 or 2).
- **Returns**: 
  - `np.ndarray`: Image with enhanced contrast.

---

### 2. `is_bright_zone_large(img, threshold, lower, higher)`
Checks if the bright area of an image is larger than a specified threshold.
- **Parameters**:
  - `img` (np.ndarray): Input image.
  - `threshold` (float): Threshold for the percentage of the bright area.
  - `lower` (int): Lower threshold for the intensity of bright pixels.
  - `higher` (int): Higher threshold for the intensity of bright pixels.
- **Returns**:
  - `bool`: True if the bright area is large, False otherwise.

---

### 3. `is_dark_zone_large(img, threshold, lower, higher)`
Checks if the dark area of an image is larger than a specified threshold.
- **Parameters**:
  - `img` (np.ndarray): Input image.
  - `threshold` (float): Threshold for the percentage of the dark area.
  - `lower` (int): Lower threshold for the intensity of dark pixels.
  - `higher` (int): Higher threshold for the intensity of dark pixels.
- **Returns**:
  - `bool`: True if the dark area is large, False otherwise.

---

### 4. `draw_bbox(img_draw, bbox, color, thickness, xywh)`
Draws a bounding box on an image.
- **Parameters**:
  - `img_draw` (np.ndarray): Image on which to draw.
  - `bbox` (List[int]): Bounding box coordinates.
  - `color` (Tuple[int, int, int]): Color of the bounding box.
  - `thickness` (int): Thickness of the bounding box.
  - `xywh` (bool): Whether the bbox is in xywh format.
- **Returns**: None. Draws directly on the image.

---

### 5. `draw_text(img_draw, text, pos, color, thickness, font_scale)`
Draws text on an image.
- **Parameters**:
  - `img_draw` (np.ndarray): Image on which to draw.
  - `text` (str): Text to draw.
  - `pos` (Tuple[int, int]): Position of the text.
  - `color` (Tuple[int, int, int]): Color of the text.
  - `thickness` (int): Thickness of the text.
  - `font_scale` (float): Font scale of the text.
- **Returns**:
  - `np.ndarray`: Image with text drawn.

---

### 6. `draw_landmarks(img_draw, landmarks, color, thickness, draw_num)`
Draws landmarks on an image.
- **Parameters**:
  - `img_draw` (np.ndarray): Image on which to draw.
  - `landmarks` (List[Tuple[int, int]]): Landmarks to draw.
  - `color` (Tuple[int, int, int]): Color of the landmarks.
  - `thickness` (int): Thickness of the landmarks.
  - `draw_num` (bool): Whether to draw the number of landmarks.
- **Returns**:
  - `np.ndarray`: Image with landmarks drawn.

---

### 7. `preprocess_2gray(img, size)`
Preprocesses an image from size (h, w, 3) to (1, 1, h, w).
- **Parameters**:
  - `img` (cv2 image): Input image.
  - `size` (Tuple[int, int]): Output size.
- **Returns**:
  - `np.ndarray`: Preprocessed image with size (1, 1, h, w).

---

### 8. `bbox_xywh2xyxy(bbox_xywh)`
Transforms the bounding box format from xywh to x1y1x2y2.
- **Parameters**:
  - `bbox_xywh` (np.ndarray): Bounding boxes (with scores), shaped (n, 4) or (n, 5).
- **Returns**:
  - `np.ndarray`: Bounding boxes (with scores), shaped (n, 4) or (n, 5).

---

### 9. `bbox_xyxy2xywh(bbox_xyxy)`
Transforms the bounding box format from x1y1x2y2 to xywh.
- **Parameters**:
  - `bbox_xyxy` (np.ndarray): Bounding boxes, shaped (n, 4).
- **Returns**:
  - `np.ndarray`: Bounding boxes, shaped (n, 4).

---

### 10. `load_onnx(model_path, cuda)`
Loads an ONNX model.
- **Parameters**:
  - `model_path` (str): Path to the ONNX model.
  - `cuda` (bool): Whether to use CUDA for the ONNX model.
- **Returns**:
  - `ort.InferenceSession`: ONNX model session.

---

### 11. `rotate_point(pt, rot_mat)`
Rotates x,y points by the given rotation matrix.
- **Parameters**:
  - `pt` (Tuple[int, int]): Point to rotate.
  - `rot_mat` (np.ndarray): Rotation matrix.
- **Returns**:
  - `Tuple[int, int]`: Rotated point.

---

### 12. `infer_onnx_model(sess, input_data)`
Loads an ONNX model and performs inference.
- **Parameters**:
  - `sess` (ort.InferenceSession): ONNX model session.
  - `input_data` (np.ndarray): Numpy array to be input to the model for inference.
- **Returns**:
  - `np.ndarray`: Output from the model after inference.

---

