import pandas as pd

RAW_FILE = "data/raw/2mass_catalog.csv"
THIN_FILE = "data/processed/stars_thin.csv"

def thin_catalog():
    print("Starting thinning...")

    df = pd.read_csv(RAW_FILE)

    df = df[["designation", "ra", "dec", "j_m"]]
    df = df.dropna()

    df.to_csv(THIN_FILE, index=False)

    print("Thinning done:", len(df), "stars")

if __name__ == "__main__":
    thin_catalog()