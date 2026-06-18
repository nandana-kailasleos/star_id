import numpy as np

from config import (
    KVECTOR_FILE,
    INDEX_FILE,
    K_ARRAY_FILE,
    M_FILE,
    Q_FILE
)


def search_angle(angle_deg, tolerance_deg=0.1):

    star_pairs = np.load(KVECTOR_FILE, allow_pickle=True)
    angles_db = np.load(INDEX_FILE)

    k = np.load(K_ARRAY_FILE)

    m = float(np.load(M_FILE))
    q = float(np.load(Q_FILE))

    angle = np.radians(angle_deg)
    tolerance = np.radians(tolerance_deg)

    lower = angle - tolerance
    upper = angle + tolerance

    jb = int(np.floor((lower - q) / m))
    jt = int(np.ceil((upper - q) / m))

    jb = max(0, jb)
    jt = min(len(k) - 1, jt)

    left = k[jb]
    right = k[jt]

    matches = []

    for idx in range(left, right):

        if lower <= angles_db[idx] <= upper:

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