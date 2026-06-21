# ============================================================
# kvector_search.py — Step 5 (runtime)
# Searches the K-vector for catalog star pairs that match
# an observed inter-star angle within a tolerance.
#
# Files are loaded ONCE at module level — fast for Pyramid
# which calls search_angle() many times per attitude solve.
#
# Returns (idx_i, idx_j, name_i, name_j, angle_deg) per match.
# Pyramid uses idx_i and idx_j to fetch unit vectors.
# ============================================================

import os
import numpy as np
from config import KVECTOR_FILE, INDEX_FILE, K_ARRAY_FILE, M_FILE, Q_FILE


def _load_kvector():
    """
    Load K-vector files from disk.
    Called once at module import if files exist,
    or manually after build_kvector.py is run.
    """
    missing = [f for f in [KVECTOR_FILE, INDEX_FILE, K_ARRAY_FILE, M_FILE, Q_FILE]
               if not os.path.exists(f)]
    if missing:
        raise FileNotFoundError(
            f"K-vector files missing: {missing}\n"
            f"Run build_kvector.py first."
        )

    pairs  = np.load(KVECTOR_FILE, allow_pickle=True)
    angles = np.load(INDEX_FILE)
    k      = np.load(K_ARRAY_FILE)
    m      = float(np.load(M_FILE))
    q      = float(np.load(Q_FILE))

    return pairs, angles, k, m, q


# ── Global cache — loaded once, reused for every search call ─
_pairs  = None
_angles = None
_k      = None
_m      = None
_q      = None


def _ensure_loaded():
    """Lazy load: load files only when first search is called."""
    global _pairs, _angles, _k, _m, _q
    if _pairs is None:
        print("Loading K-vector into memory...")
        _pairs, _angles, _k, _m, _q = _load_kvector()
        print(f"K-vector ready: {len(_angles)} pairs loaded.")


def search_angle(angle_deg, tolerance_deg=0.1):
    """
    Search for catalog star pairs matching an observed angle.

    Parameters
    ----------
    angle_deg     : float — observed angle between two stars (degrees)
    tolerance_deg : float — search tolerance in degrees (default 0.1)

    Returns
    -------
    List of tuples: (idx_i, idx_j, name_i, name_j, angle_deg)
        idx_i, idx_j  — row indices into stars_vectors.npy  (Pyramid uses these)
        name_i, name_j — star designation strings
        angle_deg      — matched angle in degrees
    """
    _ensure_loaded()

    angle     = np.radians(angle_deg)
    tolerance = np.radians(tolerance_deg)

    lower = angle - tolerance
    upper = angle + tolerance

    # ── Mortari K-vector lookup ──────────────────────────────
    # Compute index bounds directly from m and q — O(1) step
    jb = max(0, int(np.floor((lower - _q) / _m)))
    jt = min(len(_k) - 1, int(np.ceil((upper - _q) / _m)))

    left  = int(_k[jb])
    right = min(int(_k[jt]), len(_angles))   # BUG FIX: cap at array length

    # ── Scan only the narrow window ──────────────────────────
    matches = []
    for idx in range(left, right):
        if lower <= _angles[idx] <= upper:
            matches.append((
                int(_pairs[idx][0]),          # idx_i  — catalog row index
                int(_pairs[idx][1]),          # idx_j  — catalog row index
                str(_pairs[idx][2]),          # name_i — star designation
                str(_pairs[idx][3]),          # name_j — star designation
                float(np.degrees(_angles[idx]))  # matched angle in degrees
            ))

    return matches


def reload():
    """
    Force reload K-vector files from disk.
    Call this in main.py after build_kvector.py runs,
    so the new K-vector is used for searching.
    """
    global _pairs, _angles, _k, _m, _q
    _pairs = _angles = _k = _m = _q = None
    _ensure_loaded()


if __name__ == "__main__":
    try:
        angle_deg     = float(input("Enter angle in degrees: "))
        tolerance_deg = float(input("Enter tolerance in degrees (e.g. 0.1): "))

        matches = search_angle(angle_deg, tolerance_deg)

        print(f"\nTotal matches found: {len(matches)}")

        if not matches:
            print("No matches found. Try increasing tolerance.")
        else:
            print("\nMatched star pairs:\n")
            for i, (idx_i, idx_j, name_i, name_j, ang) in enumerate(matches, 1):
                print(f"  {i}. [{idx_i}] {name_i}  <-->  [{idx_j}] {name_j}"
                      f"   angle = {ang:.6f}°")

    except FileNotFoundError as e:
        print(f"ERROR: {e}")
