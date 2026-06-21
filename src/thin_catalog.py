# ============================================================
# thin_catalog.py — Step 1
# Reads raw 2MASS CSV, keeps only needed columns,
# filters by magnitude, saves clean catalog.
# Run once before everything else.
# ============================================================

import os
import pandas as pd
from config import RAW_FILE, THIN_FILE, MAG_LIMIT


def thin_catalog():
    print("=" * 45)
    print("STEP 1: Thinning catalog")
    print("=" * 45)

    # ── Load raw catalog ─────────────────────────────────────
    if not os.path.exists(RAW_FILE):
        print(f"ERROR: Raw file not found: {RAW_FILE}")
        return False

    print(f"Loading {RAW_FILE} ...")
    df = pd.read_csv(RAW_FILE)
    print(f"Raw stars loaded : {len(df)}")

    # ── Keep only required columns ───────────────────────────
    df = df[["designation", "ra", "dec", "j_m"]]

    # ── Remove rows with missing values ──────────────────────
    before_drop = len(df)
    df = df.dropna()
    print(f"Dropped NaN rows : {before_drop - len(df)}")

    # ── Magnitude filter ─────────────────────────────────────
    # Keep only stars bright enough for a satellite camera to detect.
    # j_m is J-band magnitude — lower value = brighter star.
    before_mag = len(df)
    df = df[df["j_m"] < MAG_LIMIT].reset_index(drop=True)
    print(f"Magnitude filter : kept {len(df)} of {before_mag} (j_m < {MAG_LIMIT})")

    # ── Warn if too few stars remain ─────────────────────────
    if len(df) < 1000:
        print(f"WARNING: Only {len(df)} stars remain. "
              f"Consider raising MAG_LIMIT in config.py.")

    # ── Save ─────────────────────────────────────────────────
    os.makedirs(os.path.dirname(THIN_FILE), exist_ok=True)
    df.to_csv(THIN_FILE, index=False)
    print(f"Saved           : {THIN_FILE}")
    print(f"Done. {len(df)} stars ready.\n")
    return True


if __name__ == "__main__":
    thin_catalog()
