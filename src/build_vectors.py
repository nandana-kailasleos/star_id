# ============================================================
# build_vectors.py — Step 2
# Converts each star's RA/Dec (sky coordinates) into a 3D
# unit vector on the celestial sphere.
#
# Why unit vectors?
#   dot(v1, v2) = cos(angle between stars)
#   So angle = arccos(dot(v1, v2)) — no extra trig needed later.
#
# Run once after thin_catalog.py.
# ============================================================

import os
import numpy as np
import pandas as pd
from config import THIN_FILE, VECTORS_FILE


def build_vectors():
    print("=" * 45)
    print("STEP 2: Building star vectors")
    print("=" * 45)

    # ── Load thinned catalog ─────────────────────────────────
    if not os.path.exists(THIN_FILE):
        print(f"ERROR: {THIN_FILE} not found. Run thin_catalog.py first.")
        return False

    df = pd.read_csv(THIN_FILE)
    print(f"Stars loaded: {len(df)}")

    # ── Convert RA/Dec → unit vectors ───────────────────────
    ra  = np.radians(df["ra"].values)
    dec = np.radians(df["dec"].values)

    x = np.cos(dec) * np.cos(ra)
    y = np.cos(dec) * np.sin(ra)
    z = np.sin(dec)

    vectors = np.vstack((x, y, z)).T   # shape: (N, 3)

    # ── Sanity check: all vectors must be unit length ────────
    magnitudes = np.linalg.norm(vectors, axis=1)
    if not np.allclose(magnitudes, 1.0, atol=1e-6):
        print("WARNING: Some vectors are not unit length. Check RA/Dec values.")
    else:
        print("Sanity check passed: all vectors are unit length.")

    # ── Save ─────────────────────────────────────────────────
    os.makedirs(os.path.dirname(VECTORS_FILE), exist_ok=True)
    np.save(VECTORS_FILE, vectors)
    print(f"Saved : {VECTORS_FILE}  shape={vectors.shape}")
    print("Done.\n")
    return True


if __name__ == "__main__":
    build_vectors()
