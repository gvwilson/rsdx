import random

size = 11  # change this to make a larger grid

# Make an empty grid
grid = []
for i in range(size):
    temp = []
    for j in range(size):
        temp.append(0)
    grid.append(temp)

center = size // 2  # remember to do integer division
x, y = center, center

# Move and fill until we reach the edge
moves = [[-1, 0], [1, 0], [0, -1], [0, 1]]
while True:
    grid[x][y] += 1
    m = random.choice(moves)
    x += m[0]
    y += m[1]
    if (x == 0) or (y == 0):
        break
    if (x == size - 1) or (y == size - 1):
        break

# Print as CSV
for y in range(size):
    for x in range(size):
        print(grid[x][y], end="")
        if x < size - 1:
            print(",", end="")
    print()
