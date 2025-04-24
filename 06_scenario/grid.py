from typing import ClassVar
import csv
import io
import random
from pydantic import BaseModel, Field
from utils import generic_id_generator


class Grid(BaseModel):
    """Store a grid of numbers."""

    id: str | None = Field(default=None, description="optional grid ID")
    size: int = Field(gt=0, description="grid size")
    grid: list[list] = Field(default_factory=list, description="grid values")

    def model_post_init(self, context):
        self.grid = [[0 for _ in range(self.size)] for _ in range(self.size)]

    def __getitem__(self, key):
        """Get grid element."""
        x, y = key
        return self.grid[x][y]

    def __setitem__(self, key, value):
        """Set grid element."""
        x, y = key
        self.grid[x][y] = value

    def __str__(self):
        """Convert to string."""
        output = io.StringIO()
        csv.writer(output).writerows(self.grid)
        return output.getvalue()

    _id_generator: ClassVar = generic_id_generator(lambda i: f"G{i:02d}")

    @staticmethod
    def generate(size):
        """Make and fill in a grid."""
        grid = Grid(id=next(Grid._id_generator), size=size)

        moves = [[-1, 0], [1, 0], [0, -1], [0, 1]]
        center = grid.size // 2
        size_1 = grid.size - 1
        x, y = center, center
        num = 0

        while (x != 0) and (y != 0) and (x != size_1) and (y != size_1):
            grid[x, y] += 1
            num += 1
            m = random.choice(moves)
            x += m[0]
            y += m[1]

        return grid

    @staticmethod
    def to_csv(writer, grid):
        """Convert to CSV."""
        for y in range(grid.size - 1, -1, -1):
            row = [grid[x, y] for x in range(grid.size)]
            writer.writerow(row)
