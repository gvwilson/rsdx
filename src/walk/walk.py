"""Random walk with dosage accumulation."""

import argparse
import math
import pandas as pd
from pathlib import Path
import random


CIRCLE = math.radians(360.0)


class Snail:
    """Simulate a single snail's movement."""

    def __init__(self, uid, pos, stepsize):
        """Create snail."""
        self._uid = uid
        self._pos = pos
        self._stepsize = stepsize
        self._dosage = 0.0
        self._initial_dist = math.hypot(*pos)

    def dose(self, radius):
        """Accumulate dose at current position."""
        dist = math.hypot(*self._pos)
        dose = (radius - min(dist, radius)) / radius
        self._dosage += dose

    def move(self):
        """Move the snail randomly."""
        offset = random_point(self._stepsize)
        self._pos = (self._pos[0] + offset[0], self._pos[1] + offset[1])

    def __str__(self):
        """Printable representation."""
        return f"S(u={self._uid}, x={self._pos[0]}, y={self._pos[1]}, s={self._stepsize}, d={self._dosage})"


def main():
    """Main driver."""
    args = parse_args()
    random.seed(args.seed)
    results = [walk(args, uid) for uid in range(args.reps)]
    result = pd.DataFrame(results, columns=["uid", "steps", "initial_dist", "dosage"])
    if args.outfile:
        Path(args.outfile).write_text(result.to_csv(index=False))
    else:
        print(result.to_csv(index=False))


def escape(snail, radius):
    """Has this snail escaped?"""
    return math.hypot(*snail._pos) >= radius


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--maxsteps", type=int, default=None, help="maximum number of steps"
    )
    parser.add_argument("--outfile", type=str, default=None, help="output file")
    parser.add_argument("--radius", type=float, default=None, help="radius")
    parser.add_argument("--reps", type=int, default=None, help="repetitions")
    parser.add_argument(
        "--stepsize", type=float, default=None, help="maximum step size"
    )
    parser.add_argument("--seed", type=int, default=None, help="RNG seed")
    return parser.parse_args()


def random_point(distance):
    """Pick a random point."""
    d = random.uniform(0, distance)
    angle = random.uniform(0, CIRCLE)
    return d * math.cos(angle), d * math.sin(angle)


def walk(args, uid):
    """Simulate a single walker."""
    snail = Snail(uid, random_point(args.radius), args.stepsize)
    for s in range(args.maxsteps):
        snail.move()
        snail.dose(args.radius)
        if escape(snail, args.radius):
            break
    return snail._uid, s, snail._initial_dist, snail._dosage


if __name__ == "__main__":
    main()
