## API Documentation for `similarity.py`

### 1. `base_cos_sim(vec1, vec2)`
Calculates the cosine similarity between two vectors.
- **Parameters**:
  - `vec1` (np.ndarray): First vector.
  - `vec2` (np.ndarray): Second vector.
- **Returns**:
  - `float`: Cosine similarity between the two vectors.

---

### 2. `uni_cos_sim(vec1, vec2)`
Calculates the cosine similarity between two vectors, ensuring the value is in the range [0, 1].
- **Parameters**:
  - `vec1` (np.ndarray): First vector.
  - `vec2` (np.ndarray): Second vector.
- **Returns**:
  - `float`: Cosine similarity between the two vectors, scaled to [0, 1].

---

### 3. `mat_cos_sim(mat1)`
Calculates the cosine similarity of a matrix with itself, resulting in a similarity matrix.
- **Parameters**:
  - `mat1` (np.ndarray): Input matrix.
- **Returns**:
  - `np.ndarray`: Cosine similarity matrix.

---

### 4. `cosine_similarity_mean(features)`
*(Documentation was not found in the code. Please ensure to document this function.)*
- **Parameters**:
  - `features` (np.ndarray): Feature matrix.
- **Returns**: 
  - *(Return type and description were not found in the code.)*

---

### 5. `get_mean_cosine_similarity(image_names, features)`
Calculates the mean cosine similarity of a matrix.
- **Parameters**:
  - `image_names` (List[str]): List of image names.
  - `features` (np.ndarray): Feature matrix.
- **Returns**: 
  - *(Return type and description were not found in the code.)*

---

### 6. `feature_cross_sims(mat_dict, threshold)`
Performs a cross calculation of the similarity matrix and returns indices of images that are similar to each other. Input is a dictionary of feature arrays indexed by ID, and the output is a dictionary where keys are ID pairs and values are lists of index pairs from the corresponding ID pair that are similar based on the threshold.
- **Parameters**:
  - `mat_dict` (Dict[str, np.ndarray]): Dictionary with IDs as keys and feature arrays as values.
  - `threshold` (float): Threshold for determining similarity.
- **Returns**:
  - `Dict[Tuple[str, str], List[Tuple[int, int]]]`: Dictionary with ID pairs as keys and lists of index pairs that are similar based on the threshold.

---

