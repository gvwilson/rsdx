"""Generate random plates with some formatting gotchas.

Default output is CSV that looks like:

    Weyland-Yutani 470 1879,,,,
    Recorded,2023-10-23:08:21:45,,,
    ,,,,
    ,A,B,C,D
    1,1.67,2.35,4.17,2.75
    2,2.78,2.52,3.23,1.81
    3,0.91,1.35,3.73,1.50
    4,3.34,3.46,3.70,0.77
    ,,,,
    Checksum,5a7b,,,

Options:

-   empty: fraction of empty cells
-   out: specify output file
-   seed: specify random number seed

"""

import hashlib
import random

CHECKSUM_RANGE = 2**16
MODEL = "Weyland-Yutani 470"
PLATE_HEIGHT = 6
PLATE_WIDTH = 8
PLATE_COORDS = list(range(PLATE_WIDTH * PLATE_HEIGHT))
MAX_READING = 5.0


def make_plate(seed, empty):
    """Main driver."""
    if seed is not None:
        random.seed(seed)
    head = head_generate()
    body = body_generate(empty)
    checksum = body_calculate_checksum(body)
    foot = foot_generate(checksum)
    return csv_normalize([*head, *body, *foot])


def body_add_titles(readings):
    """Make column titles for plate readings."""
    title_row = ["", *[chr(ord("A") + col) for col in range(PLATE_WIDTH)]]
    readings = [[str(i + 1), *r] for (i, r) in enumerate(readings)]
    return [title_row, *readings]


def body_calculate_checksum(body):
    """Calculate SHA256 checksum for body."""
    m = hashlib.sha256()
    for row in body:
        for val in row:
            m.update(bytes(val, "utf-8"))
    digest = int(m.hexdigest(), base=16) % CHECKSUM_RANGE
    return f"{digest:04x}"


def body_empty_readings(readings, empty):
    """Replace some readings with empty."""
    num_empty = int(empty * len(PLATE_COORDS))
    coords = random.sample(PLATE_COORDS, num_empty)
    for c in coords:
        col = c % PLATE_WIDTH
        row = c // PLATE_WIDTH
        readings[row][col] = ""
    return readings


def body_generate(empty):
    """Make body of plate."""
    readings = body_generate_readings()
    readings = body_empty_readings(readings, empty)
    readings = body_add_titles(readings)
    return readings


def body_generate_readings():
    """Make table of plate readings."""
    return [
        [f"{(random.random() * MAX_READING):.02f}" for _ in range(PLATE_WIDTH)]
        for row in range(PLATE_HEIGHT)
    ]


def csv_normalize(rows):
    required = max(len(r) for r in rows)
    for row in rows:
        row.extend([""] * (required - len(row)))
    return rows


def foot_generate(checksum):
    """Make foot of plate."""
    return [
        [],
        ["Checksum", checksum],
    ]


def head_generate():
    """Make head of plate."""
    return [
        [f"{MODEL}"],
        [],
    ]


if __name__ == "__main__":
    import csv
    import sys

    plate = make_plate(int(sys.argv[1]), float(sys.argv[2]))
    csv.writer(sys.stdout).writerows(plate)
