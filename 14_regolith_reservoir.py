import numpy as np

# load the data
with open("data/14.txt", "r") as f:
    paths = f.read().split("\n")


cave_map = np.zeros((1000, 1000)) # 0 is air
sand_init_coords = (0, 500)
cave_map[sand_init_coords] = -1 # sand
deepest_rock = 0

for path in paths:
    # read coords of this path
    coords = [np.array(list(map(int, e.split(",")))) for e in path.split(" -> ")]

    # draw the path
    for i in range(len(coords)-1):
        if coords[i][0] == coords[i+1][0]:
            # vertical path
            y_bounds = min(coords[i][1], coords[i+1][1]), max(coords[i][1], coords[i+1][1])+1
            cave_map[list(range(*y_bounds)), coords[i][0]] = 1 # rock
        else:
            # horizontal path
            x_bounds = min(coords[i][0], coords[i+1][0]), max(coords[i][0], coords[i+1][0])+1
            cave_map[coords[i][1], list(range(*x_bounds))] = 1

        deepest_rock = max(deepest_rock, coords[i][1], coords[i+1][1])

# part a

def simulate_sand(cave_map, sand_init_coords=(0, 500), part_a=True):

    # attempt to move sand down
    def move_sand(sand_coord):
        # check if there is a rock/sand below
        if cave_map[sand_coord[0]+1, sand_coord[1]] == 0:
            return sand_coord[0]+1, sand_coord[1]
        # check if there is a rock/sand to lower left
        if cave_map[sand_coord[0]+1, sand_coord[1]-1] == 0:
            return sand_coord[0]+1, sand_coord[1]-1
        # check if there is a rock/sand to lower right
        if cave_map[sand_coord[0]+1, sand_coord[1]+1] == 0:
            return sand_coord[0]+1, sand_coord[1]+1
        else:
            # cannot move sand
            return None

    stop_loop = False

    sand_coord = list(sand_init_coords)
    while not stop_loop:
        if sand_coord[0] == 10 and sand_coord[1] == 493:
            pass
        new_sand_coord = move_sand(sand_coord)
        if new_sand_coord is None:
            cave_map[tuple(sand_coord)] = -2 # settled sand

            if not part_a and cave_map[tuple(sand_init_coords)] == -2:
                stop_loop = True

            sand_coord = list(sand_init_coords)
        else:
            cave_map[tuple(new_sand_coord)] = -1 # sand
            cave_map[tuple(sand_coord)] = 0 # air
            sand_coord = new_sand_coord

            # stopping condition
            if part_a and sand_coord[0] > deepest_rock:
                stop_loop = True
    return cave_map

part_a_map = simulate_sand(cave_map.copy())
# count the settled sand
print(np.sum(part_a_map == -2))

# part b
floor_y = deepest_rock + 2
cave_map[floor_y, :] = 1 # rock floor
part_b_map = simulate_sand(cave_map.copy(), part_a=False)
print(np.sum(part_b_map == -2))