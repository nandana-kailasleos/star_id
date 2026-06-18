import numpy as np
from config import KVECTOR_FILE, INDEX_FILE


def search_angle(angle_deg, tolerance_deg=0.1):

    # Load database
    star_pairs = np.load(KVECTOR_FILE, allow_pickle=True)
    angles_db = np.load(INDEX_FILE)

    # Convert to radians
    angle = np.radians(angle_deg)
    tolerance = np.radians(tolerance_deg)

    # Search interval
    lower = angle - tolerance
    upper = angle + tolerance

    # Find matching range
    left = np.searchsorted(angles_db, lower)
    right = np.searchsorted(angles_db, upper)

    matches = []

    for idx in range(left, right):

        matches.append(
            (
                star_pairs[idx][0],
                star_pairs[idx][1],
                np.degrees(angles_db[idx])
            )
        )

    return matches


if __name__ == "__main__":

    angle_deg = float(input("Enter angle in degrees: "))
    tolerance_deg = float(input("Enter tolerance in degrees: "))

    matches = search_angle(angle_deg, tolerance_deg)

    print("\nTotal matches found:", len(matches))

    print("\nMatched star pairs:\n")

    if len(matches) == 0:

        print("No matches found.")

    else:

        for i, (star1, star2, ang) in enumerate(matches, start=1):

            print(
                f"{i}. {star1} <--> {star2}    angle = {ang:.6f} deg"
            )