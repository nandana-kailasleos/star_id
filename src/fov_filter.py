import numpy as np
import os
from config import VECTORS_FILE


def fov_filter(vectors, center_vec, fov_deg):

    fov_rad = np.radians(fov_deg)

    dots = np.dot(vectors, center_vec)

    return np.where(dots >= np.cos(fov_rad))[0]


def run_fov_filter():

    print("Loading vectors...")

    vectors = np.load(VECTORS_FILE)

    # Temporary fixed camera direction
    center_vec = np.array([0, 0, 1])

    fov = float(input("Enter FOV (2 to 5 degrees): "))

    if not (2 <= fov <= 5):
        print("Error: FOV must be between 2 and 5 degrees")
        return

    indices = fov_filter(vectors, center_vec, fov)

    fov_vectors = vectors[indices]

    print("Total stars:", len(vectors))
    print("Stars in FOV:", len(fov_vectors))

    os.makedirs("data/cache", exist_ok=True)

    np.save("data/cache/fov_subset.npy", fov_vectors)
    np.save("data/cache/fov_indices.npy", indices)

    print("Saved:")
    print("data/cache/fov_subset.npy")
    print("data/cache/fov_indices.npy")


if __name__ == "__main__":
    run_fov_filter()