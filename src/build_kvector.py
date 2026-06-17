import numpy as np
import os
from config import KVECTOR_FILE, INDEX_FILE, CACHE_FOV

def build_kvector():

    print("Loading FOV-filtered vectors...")

    # ✅ IMPORTANT: using FOV subset, NOT full catalog
    vectors = np.load(CACHE_FOV)
    n = len(vectors)

    print("Stars in FOV:", n)

    angles = []

    print("Computing pairwise angles...")

    for i in range(n):
        vi = vectors[i]

        for j in range(i + 1, n):

            dot = np.dot(vi, vectors[j])
            dot = np.clip(dot, -1.0, 1.0)

            angle = np.arccos(dot)

            angles.append(angle)

    angles = np.array(angles)

    print("Total pairs:", len(angles))

    print("Sorting angles...")

    angles.sort()

    k = np.arange(len(angles))

    os.makedirs("data/processed", exist_ok=True)

    np.save(KVECTOR_FILE, k)
    np.save(INDEX_FILE, angles)

    print("K-vector built successfully!")

if __name__ == "__main__":
    build_kvector()