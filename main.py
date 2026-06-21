# ============================================================
# main.py — Runtime entry point
#
# EXECUTION ORDER (run each step only once unless data changes):
#
#   python src/thin_catalog.py     ← Step 1  (run once)
#   python src/build_vectors.py    ← Step 2  (run once)
#   python src/fov_filter.py       ← Step 3  (run when boresight/FOV changes)
#   python src/build_kvector.py    ← Step 4  (run after fov_filter)
#   python main.py                 ← Step 5  (runtime search)
#
# main.py only does Step 3 + search at runtime.
# Steps 1 and 2 are one-time setup — run them separately first.
# ============================================================

import sys
import os

# ── Make sure src/ is on the path ────────────────────────────
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))


def main():
    print("=" * 45)
    print(" LEOs MEERA — Star Tracker K-Vector")
    print("=" * 45)
    print()
    print("NOTE: Before running this, make sure you have already run:")
    print("  python src/thin_catalog.py")
    print("  python src/build_vectors.py")
    print()

    # ── Step 3: FOV filter ───────────────────────────────────
    # Asks user for boresight and FOV, saves fov_subset.npy
    from src.fov_filter import run_fov_filter
    ok = run_fov_filter()
    if not ok:
        print("FOV filter failed. Exiting.")
        return

    # ── Step 4: Build K-vector ───────────────────────────────
    # Must run after fov_filter so it uses the fresh FOV subset.
    from src.build_kvector import build_kvector
    ok = build_kvector()
    if not ok:
        print("K-vector build failed. Exiting.")
        return

    # ── Step 5: Search ───────────────────────────────────────
    # K-vector files now exist — safe to import kvector_search.
    from src.kvector_search import search_angle, reload

    # Reload ensures this session uses the just-built K-vector,
    # not any stale cached version from a previous run.
    reload()

    print("=" * 45)
    print("K-VECTOR SEARCH")
    print("=" * 45)
    print("Enter the angle you observed between two stars in the camera image.")
    print()

    try:
        angle_deg     = float(input("Observed angle (degrees)        : "))
        tolerance_deg = float(input("Tolerance      (degrees, e.g 0.1): "))
    except ValueError:
        print("ERROR: Enter numeric values.")
        return

    if tolerance_deg <= 0:
        print("ERROR: Tolerance must be greater than 0.")
        return

    # ── Run search ───────────────────────────────────────────
    matches = search_angle(angle_deg, tolerance_deg)

    print(f"\nMatches found: {len(matches)}")

    if not matches:
        print("No matches. Try increasing tolerance slightly.")
        return

    print("\nMatched catalog star pairs:")
    print("-" * 65)
    for i, (idx_i, idx_j, name_i, name_j, ang) in enumerate(matches, 1):
        print(f"  {i:2d}. [{idx_i:6d}] {name_i}  <-->  [{idx_j:6d}] {name_j}"
              f"   {ang:.6f}°")
    print("-" * 65)
    print()
    print("These index numbers [idx] are the row positions in stars_vectors.npy.")
    print("Pyramid algorithm will use them to fetch unit vectors for attitude solve.")


if __name__ == "__main__":
    main()
