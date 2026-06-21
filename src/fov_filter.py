# ============================================================
# fov_filter.py — Step 3
# Filters the full star catalog to only the stars visible
# inside the camera's cone of vision (FOV).
#
# The boresight vector tells which direction the camera points.
# For Pyramid algorithm: boresight comes from attitude estimate.
# For testing now: user enters it manually as (bx, by, bz).
#
# Run after build_vectors.py, before build_kvector.py.
# ============================================================

import os
import numpy as np
from config import VECTORS_FILE, CACHE_FOV, CACHE_FOV_IDX, FOV_MIN, FOV_MAX


def fov_filter(vectors, center_vec, fov_deg):
    """
    Core filter function.
    Returns indices of stars inside the FOV cone.

    Parameters
    ----------
    vectors    : (N, 3) array of unit star vectors
    center_vec : (3,) unit vector — camera pointing direction (boresight)
    fov_deg    : float — half-angle of FOV cone in degrees

    Returns
    -------
    indices : 1D array of row indices into `vectors`
    """
    fov_rad = np.radians(fov_deg)
    dots    = np.dot(vectors, center_vec)          # dot product all stars at once
    return np.where(dots >= np.cos(fov_rad))[0]    # stars inside cone


def run_fov_filter():
    """
    Interactive runner.
    Asks user for boresight direction and FOV,
    runs the filter, saves results to cache.

    NOTE for Pyramid integration:
    Replace this function's inputs with the attitude estimate output.
    The rest of the function stays the same.
    """
    print("=" * 45)
    print("STEP 3: FOV filtering")
    print("=" * 45)

    # ── Load full star vectors ───────────────────────────────
    if not os.path.exists(VECTORS_FILE):
        print(f"ERROR: {VECTORS_FILE} not found. Run build_vectors.py first.")
        return False

    vectors = np.load(VECTORS_FILE)
    print(f"Total catalog stars: {len(vectors)}")

    # ── Get boresight from user ──────────────────────────────
    # This is the camera pointing direction as a 3D vector.
    # Example: [0, 0, 1] = pointing at north celestial pole.
    # In a real satellite this comes from gyro/attitude sensor.
    print("\nEnter camera boresight direction (3D unit vector).")
    print("Example — north pole: bx=0, by=0, bz=1")
    try:
        bx = float(input("  bx: "))
        by = float(input("  by: "))
        bz = float(input("  bz: "))
    except ValueError:
        print("ERROR: Enter numeric values for boresight.")
        return False

    center_vec = np.array([bx, by, bz])

    # ── Normalize boresight to unit vector ───────────────────
    norm = np.linalg.norm(center_vec)
    if norm < 1e-9:
        print("ERROR: Boresight vector cannot be zero.")
        return False
    center_vec = center_vec / norm
    print(f"Boresight (normalized): {center_vec.round(6)}")

    # ── Get FOV from user ────────────────────────────────────
    try:
        fov = float(input(f"\nEnter FOV ({FOV_MIN} to {FOV_MAX} degrees): "))
    except ValueError:
        print("ERROR: Enter a numeric FOV value.")
        return False

    if not (FOV_MIN <= fov <= FOV_MAX):
        print(f"ERROR: FOV must be between {FOV_MIN} and {FOV_MAX} degrees.")
        return False

    # ── Run filter ───────────────────────────────────────────
    indices    = fov_filter(vectors, center_vec, fov)
    fov_vectors = vectors[indices]

    print(f"\nStars in FOV ({fov}°): {len(fov_vectors)}")

    if len(fov_vectors) < 4:
        print("WARNING: Fewer than 4 stars in FOV. "
              "Pyramid algorithm needs at least 4. Try a wider FOV.")

    # ── Save cache ───────────────────────────────────────────
    os.makedirs("data/cache", exist_ok=True)
    np.save(CACHE_FOV,     fov_vectors)   # (n, 3) unit vectors in FOV
    np.save(CACHE_FOV_IDX, indices)       # their row indices in full catalog

    print(f"Saved: {CACHE_FOV}")
    print(f"Saved: {CACHE_FOV_IDX}")
    print("Done.\n")
    return True


if __name__ == "__main__":
    run_fov_filter()
