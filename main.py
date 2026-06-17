import numpy as np
from src.fov_filter import fov_filter

from config import (
    VECTORS_FILE,
    KVECTOR_FILE,
    INDEX_FILE
)

vectors = np.load(VECTORS_FILE)
kvector = np.load(KVECTOR_FILE)
angles = np.load(INDEX_FILE)

# example camera direction (boresight)
center_vec = np.array([1, 0, 0])

# FOV filter (you will vary 2°–5° here)
stars = fov_filter(vectors, center_vec, fov_deg=5)

print("Stars in FOV:", len(stars))