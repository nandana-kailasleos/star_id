# ============================================================
# config.py — single source of truth for all file paths
# and constants used across the pipeline
# ============================================================

# ── Raw input ────────────────────────────────────────────────
RAW_FILE = "data/raw/2mass_catalog.csv"

# ── Processed outputs ────────────────────────────────────────
THIN_FILE       = "data/processed/stars_thin.csv"
VECTORS_FILE    = "data/processed/stars_vectors.npy"
KVECTOR_FILE    = "data/processed/kvector.npy"
INDEX_FILE      = "data/processed/star_index.npy"
K_ARRAY_FILE    = "data/processed/k_array.npy"
M_FILE          = "data/processed/m.npy"
Q_FILE          = "data/processed/q.npy"

# ── FOV cache (written by fov_filter, read by build_kvector) ─
CACHE_FOV       = "data/cache/fov_subset.npy"
CACHE_FOV_IDX   = "data/cache/fov_indices.npy"

# ── Runtime constants ────────────────────────────────────────
FOV_MIN  = 2.0   # degrees — minimum allowed FOV
FOV_MAX  = 5.0   # degrees — maximum allowed FOV

# Magnitude limit: only stars brighter than this are kept.
# Your 2MASS data ranges from j_m=4.89 to j_m=7.0.
# 6.5 keeps ~50k bright stars a real camera can reliably detect.
MAG_LIMIT = 6.5
