import numpy as np
from config import KVECTOR_FILE, INDEX_FILE

def search_stars(observed_vectors):

    print("Loading K-vector database...")

    kvector = np.load(KVECTOR_FILE)
    angles_db = np.load(INDEX_FILE)

    n = len(observed_vectors)

    print("Observed stars:", n)

    observed_angles = []

    # compute observed pair angles
    for i in range(n):
        for j in range(i + 1, n):

            dot = np.dot(observed_vectors[i], observed_vectors[j])
            dot = np.clip(dot, -1.0, 1.0)

            angle = np.arccos(dot)
            observed_angles.append(angle)

    observed_angles = np.sort(np.array(observed_angles))

    print("Matching with database...")

    # simple matching (baseline version)
    matches = []

    for angle in observed_angles:
        idx = np.argmin(np.abs(angles_db - angle))
        matches.append(idx)

    print("Matches found:", len(matches))

    return matches


if __name__ == "__main__":

    # dummy test input (replace later with real camera stars)
    test_vectors = np.array([
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1]
    ])

    search_stars(test_vectors)