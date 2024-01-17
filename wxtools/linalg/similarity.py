"""""""""""""""""""""""""""""
Project: wxtools
Author: Terance Jiang
Date: 1/16/2024
"""""""""""""""""""""""""""""
import numpy as np
from tqdm import tqdm


def base_cos_sim(vec1: np.ndarray, vec2: np.ndarray) -> float:
    """
    calculate cosine similarity between two vectors
    :param vec1:  vector 1
    :param vec2:  vector 2
    :return:  cosine similarity
    """
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))


def uni_cos_sim(vec1: np.ndarray, vec2: np.ndarray) -> float:
    """
    calculate cosine similarity between two vectors, return value is in [0, 1]
    :param vec1:  vector 1
    :param vec2:  vector 2
    :return:  cosine similarity in [0, 1]
    """
    return np.dot(vec1, vec2) / ((np.linalg.norm(vec1) * np.linalg.norm(vec2)) * 2 + 1e-6) + 0.5


def mat_cos_sim(mat1: np.ndarray) -> np.ndarray:
    """
    calculate cosine similarity of a matrix
    :param mat1:  matrix
    :return:  cosine similarity matrix
    """
    mat1_norm = np.linalg.norm(mat1, axis=1)
    normed_features = mat1 / mat1_norm[:, np.newaxis]
    similarity_matrix = np.dot(normed_features, normed_features.T)

    return similarity_matrix


def feature_cross_sims(mat_dict, threshold=0.9):
    """
    cross calculation of similarity matrix.
    return index of images that are similar to each other.

    input is a dict of {id: np.array n*x(x dim features)}
    output is a dict where key = id pairs, value = list of pair index from key id pair.

    such as:
    input:
    {'id1': np.array n1*x,
    'id2': np.array n2*x
    }
    output :
    {('id1', 'id2'):
        [(10, 225),  id1[10] is similar to id2[225]
        (10, 228), id1[10] is similar to id2[228]
        (10, 229)...]
    }

    :param mat_dict: {id: {np.array n*x(x dim features)}}
    :return:
    """
    features = []
    id_indices = []
    id_keys = []
    feature_indices = []
    output = {}

    for idx, (key, val) in tqdm(enumerate(mat_dict.items())):
        for feature_id, feature in enumerate(val):
            features.append(feature)  # feature is a vector
            id_indices.append(idx)  # id_indices is a list of id index
            feature_indices.append(feature_id)  # feature_indices is a list of feature index
            id_keys.append(key)  # id_keys is a list of id
    features = np.vstack(features)

    similarity_matrix = mat_cos_sim(features)

    for i, id1 in tqdm(id_keys):
        for j, id2 in enumerate(id_keys):
            if i != j:
                mask_i = np.array(id_indices) == i
                mask_j = np.array(id_indices) == j
                cos_similarities = similarity_matrix[np.ix_(mask_i, mask_j)]

                # Filtering based on threshold
                high_similarity_indices = np.where(cos_similarities > threshold)
                feature_pairs = [(feature_indices[x], feature_indices[y]) for x, y in zip(*high_similarity_indices)]
                if feature_pairs:
                    output[(id1, id2)] = feature_pairs

    return output
