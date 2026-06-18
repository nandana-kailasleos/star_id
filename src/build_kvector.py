import numpy as np
import pandas as pd
import os

from config import (
    CACHE_FOV,
    KVECTOR_FILE,
    INDEX_FILE,
    THIN_FILE,
    K_ARRAY_FILE,
    M_FILE,
    Q_FILE
)


def build_kvector():

    print("Loading FOV vectors...")

    vectors = np.load(CACHE_FOV)

    stars_df = pd.read_csv(THIN_FILE)

    indices = np.load("data/cache/fov_indices.npy")

    star_ids = stars_df["designation"].values[indices]

    n = len(vectors)

    print("Stars:", n)

    angles = []
    star_pairs = []

    print("Computing pairwise angles...")

    for i in range(n):

        for j in range(i + 1, n):

            dot = np.dot(vectors[i], vectors[j])
            dot = np.clip(dot, -1.0, 1.0)

            angle = np.arccos(dot)

            angles.append(angle)

            star_pairs.append(
                (
                    star_ids[i],
                    star_ids[j]
                )
            )

    angles = np.array(angles)
    star_pairs = np.array(star_pairs)

    print("Total pairs:", len(angles))

    # Sort
    order = np.argsort(angles)

    angles = angles[order]
    star_pairs = star_pairs[order]

    # Mortari parameters
    epsilon = np.radians(0.1)

    z0 = angles[0]
    zn = angles[-1]

    m = (zn - z0 + 2 * epsilon) / (len(angles) - 1)

    q = z0 - m - epsilon

    # Build K-vector
    k = np.zeros(len(angles) + 1, dtype=int)

    for j in range(len(k)):

        z = q + j * m

        k[j] = np.searchsorted(angles, z)

    os.makedirs("data/processed", exist_ok=True)

    np.save(KVECTOR_FILE, star_pairs)
    np.save(INDEX_FILE, angles)

    np.save(K_ARRAY_FILE, k)
    np.save(M_FILE, m)
    np.save(Q_FILE, q)

    print("Mortari K-vector built successfully!")


if __name__ == "__main__":
    build_kvector()