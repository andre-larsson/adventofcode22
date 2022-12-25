from collections import defaultdict

import numpy as np

with open("data/23.txt") as f:
    lines = f.readlines()

# create grid
padding = 100
grid_padded = np.zeros(((len(lines)+2*padding),len(lines[0])+2*padding), dtype=bool)

directions_init = [(-1,0), (1,0), (0,-1), (0,1)] # up, down, left, right

# fill grid
for i, line in enumerate(lines):
    for j, c in enumerate(line):
        if c == "#":
            grid_padded[i+padding,j+padding] = True
        else:
            grid_padded[i+padding,j+padding] = False


def move_elves(grid_padded, max_count=9999999):

    planned_moves = defaultdict(list)
    i = 0

    while i < max_count:
        index = i % 4
        directions = directions_init[index:] + directions_init[:index]
        for elf_coord in np.argwhere(grid_padded):
            # no other elves nearby
            if sum(grid_padded[elf_coord[0]-1:elf_coord[0]+2, elf_coord[1]-1:elf_coord[1]+2].flatten()) == 1:
                continue

            for d in directions:
                if d[0] == 0:
                    check_pos = [(elf_coord[0]-1, elf_coord[1]+d[1]),
                                  (elf_coord[0], elf_coord[1]+d[1]),
                                 (elf_coord[0]+1, elf_coord[1]+d[1])]
                else:
                    check_pos = [(elf_coord[0]+d[0], elf_coord[1]-1),
                                 (elf_coord[0]+d[0], elf_coord[1]),
                                 (elf_coord[0]+d[0], elf_coord[1]+1)]


                empty_space = all([not grid_padded[x[0],x[1]] for x in check_pos])
                if empty_space:
                    # attemp move to new_pos
                    planned_moves[check_pos[1]].append(tuple(elf_coord))
                    break

        # move elves
        for new_pos, elves in planned_moves.items():
            if len(elves) < 2: # move elf
                grid_padded[new_pos] = True
                grid_padded[elves[0]] = False
            else: # noone can move
                pass

        if len(planned_moves) == 0:
            i += 1
            break
        else:
            planned_moves = defaultdict(list)
            i += 1

    return grid_padded, i

# simulate for 10 rounds
new_grid, _ = move_elves(grid_padded.copy(), 10)

# find smallest rectangle containing all elves
coord_array = np.argwhere(new_grid)
minv = np.min(coord_array, axis=0)
maxv = np.max(coord_array, axis=0)
min_rect = new_grid[minv[0]:maxv[0]+1,minv[1]:maxv[1]+1]
num_empty = np.sum(min_rect == False)

print("Answer part one:", num_empty)

# part two

# simulate until no more moves
new_grid, num_rounds = move_elves(grid_padded.copy())

print("Answer part two:", num_rounds)