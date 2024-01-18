"""""""""""""""""""""""""""""
Project: wxtools
Author: Terance Jiang
Date: 1/17/2024
"""""""""""""""""""""""""""""

import numpy as np

from wxtools.linalg.similarity import get_mean_cosine_similarity


# The function definitions from the previous message would go here

def test_cosine_similarity():
    # Create a small set of artificial feature vectors
    image_names = ['image1', 'image2', 'image3']
    features = np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 1]
    ], dtype=float)

    # Normalize the features manually for calculating expected results
    features_normalized = features / np.linalg.norm(features, axis=1, keepdims=True)

    # Calculate the cosine similarities using the function
    result = get_mean_cosine_similarity(image_names, features)

    # Manually compute the expected cosine similarities
    expected_cosine_sim_matrix = np.dot(features_normalized, features_normalized.T)
    np.fill_diagonal(expected_cosine_sim_matrix, 0)
    expected_mean_cosine_sim = np.mean(expected_cosine_sim_matrix, axis=1)
    expected_result = dict(zip(image_names, expected_mean_cosine_sim))

    # Compare the results
    for img in image_names:
        assert np.isclose(result[img],
                          expected_result[img]), f"Cosine similarity for {img} did not match the expected value."

    print("All tests passed!")


# Run the test case
test_cosine_similarity()