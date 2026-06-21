# ============================================================
# build_kvector.py — Step 4
# Builds Mortari's K-vector index from the FOV star subset.
#
# What it does:
#   1. Computes angular separation between every pair of FOV stars
#   2. Sorts all pairs by angle
#   3. Builds K-vector lookup table (m, q, k[]) for O(1) search
#
# Each pair is stored as (idx_i, idx_j, name_i, name_j) so the
# Pyramid algorithm can fetch unit vectors using the index numbers.
#
# Run after fov_filter.py. Re-run whenever FOV or boresight changes.
# ============================================================

import os
import numpy as np
import pandas as pd
from config import (
    CACHE_FOV, CACHE_FOV_IDX,
    KVECTOR_FILE, INDEX_FILE,
    THIN_FILE,
    K_ARRAY_FILE, M_FILE, Q_FILE
)


def build_kvector():
    print("=" * 45)
    print("STEP 4: Building K-vector")
    print("=" * 45)

    # ── Load FOV subset ──────────────────────────────────────
    if not os.path.exists(CACHE_FOV):
        print(f"ERROR: {CACHE_FOV} not found. Run fov_filter.py first.")
        return False
    if not os.path.exists(CACHE_FOV_IDX):
        print(f"ERROR: {CACHE_FOV_IDX} not found. Run fov_filter.py first.")
        return False

    vectors = np.load(CACHE_FOV)           # (n, 3) — FOV star unit vectors
    indices = np.load(CACHE_FOV_IDX)       # (n,)   — their catalog row numbers

    # ── Load star names using catalog indices ────────────────
    stars_df = pd.read_csv(THIN_FILE)
    star_ids = stars_df["designation"].values[indices]

    n = len(vectors)
    print(f"FOV stars         : {n}")
    print(f"Pairs to compute  : {n * (n - 1) // 2}")

    if n < 2:
        print("ERROR: Need at least 2 stars in FOV to build K-vector.")
        return False

    # ── Compute all pairwise angles ──────────────────────────
    angles     = []
    star_pairs = []

    print("Computing pairwise angles...")
    for i in range(n):

        if i % 10 == 0 and i > 0:
            print(f"  Processing star {i + 1}/{n} ...")

        for j in range(i + 1, n):

            dot   = np.dot(vectors[i], vectors[j])
            dot   = np.clip(dot, -1.0, 1.0)       # guard against float errors
            angle = np.arccos(dot)

            angles.append(angle)

            # Store (catalog_index_i, catalog_index_j, name_i, name_j)
            # Pyramid algorithm uses catalog indices to fetch unit vectors.
            star_pairs.append((
                int(indices[i]),    # row index in stars_vectors.npy  ← Pyramid uses this
                int(indices[j]),    # row index in stars_vectors.npy  ← Pyramid uses this
                star_ids[i],        # human-readable star name
                star_ids[j]         # human-readable star name
            ))

    angles     = np.array(angles)
    star_pairs = np.array(star_pairs, dtype=object)   # mixed types need object dtype

    print(f"Total pairs built : {len(angles)}")
    print(f"Angle range       : {np.degrees(angles.min()):.4f}° "
          f"to {np.degrees(angles.max()):.4f}°")

    # ── Sort by angle (required for K-vector) ────────────────
    order      = np.argsort(angles)
    angles     = angles[order]
    star_pairs = star_pairs[order]

    # ── Mortari K-vector parameters ──────────────────────────
    # m and q define a linear mapping: angle → index in sorted list
    # This allows O(1) lookup: given query angle, compute jb and jt directly.
    epsilon = np.radians(0.1)          # small guard margin

    z0 = angles[0]
    zn = angles[-1]

    m = (zn - z0 + 2 * epsilon) / (len(angles) - 1)
    q = z0 - m - epsilon

    # ── Build K-vector array k[] ─────────────────────────────
    # k[j] = first index in angles[] where angles[idx] >= q + j*m
    k = np.zeros(len(angles) + 1, dtype=int)
    for j in range(len(k)):
        z    = q + j * m
        k[j] = int(np.searchsorted(angles, z))

    # ── Save all outputs ─────────────────────────────────────
    os.makedirs("data/processed", exist_ok=True)

    np.save(KVECTOR_FILE, star_pairs)   # (pairs, 4): idx_i, idx_j, name_i, name_j
    np.save(INDEX_FILE,   angles)       # sorted angles in radians
    np.save(K_ARRAY_FILE, k)            # K-vector lookup array
    np.save(M_FILE,       m)            # Mortari slope
    np.save(Q_FILE,       q)            # Mortari intercept

    print(f"\nSaved: {KVECTOR_FILE}")
    print(f"Saved: {INDEX_FILE}")
    print(f"Saved: {K_ARRAY_FILE}")
    print(f"Mortari m = {m:.8f} rad")
    print(f"Mortari q = {q:.8f} rad")
    print("K-vector built successfully!\n")
    return True


if __name__ == "__main__":
    build_kvector()
