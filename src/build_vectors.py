import numpy as np
import pandas as pd

from config import THIN_FILE, VECTORS_FILE

def build_vectors():
    df = pd.read_csv(THIN_FILE)

    ra = np.radians(df["ra"])
    dec = np.radians(df["dec"])

    x = np.cos(dec) * np.cos(ra)
    y = np.cos(dec) * np.sin(ra)
    z = np.sin(dec)

    vectors = np.vstack((x, y, z)).T

    np.save(VECTORS_FILE, vectors)

    print("Vectors created:", vectors.shape)

if __name__ == "__main__":
    build_vectors()