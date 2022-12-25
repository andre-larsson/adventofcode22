import re
from functools import cache

with open("data/22.txt") as f:
    lines = f.readlines()

map_dict = dict()

for i, line in enumerate(lines[:-1]):
    if len(line) == 0:
        continue
    for j, c in enumerate(line):
        if c != " " and c != "\n":
            map_dict[(i+1,j+1)] = c

p = re.compile('\d+|\D')
moves = p.findall(lines[-1])

all_coords = list(map_dict.keys())
current_pos = sorted(all_coords)[0]
facing = 0  # 0 = right, 1 = down, 2 = left, 3 = up

max_row = max([x[0] for x in all_coords])
max_col = max([x[1] for x in all_coords])


@cache
def get_next_pos(current_pos, facing):
    if facing == 0:  # right
        new_pos = (current_pos[0], current_pos[1] + 1)
        row = [x[1] for x in all_coords if x[0] == current_pos[0]]
        if new_pos not in all_coords:
            min_col = min(row)
            new_pos = (current_pos[0], min_col)
        if map_dict[new_pos] == "#":
            return current_pos
        else:
            return new_pos
    elif facing == 1:  # down
        new_pos = (current_pos[0] + 1, current_pos[1])
        col = [x[0] for x in all_coords if x[1] == current_pos[1]]
        if new_pos not in all_coords:
            min_row = min(col)
            new_pos = (min_row, current_pos[1])
        if map_dict[new_pos] == "#":
            return current_pos
        else:
            return new_pos
    elif facing == 2:  # left
        new_pos = (current_pos[0], current_pos[1] - 1)
        row = [x[1] for x in all_coords if x[0] == current_pos[0]]
        if new_pos not in all_coords:
            max_col = max(row)
            new_pos = (current_pos[0], max_col)
        if map_dict[new_pos] == "#":
            return current_pos
        else:
            return new_pos
    else: # up
        new_pos = (current_pos[0] - 1, current_pos[1])
        col = [x[0] for x in all_coords if x[1] == current_pos[1]]
        if new_pos not in all_coords:
            max_row = max(col)
            new_pos = (max_row, current_pos[1])
        if map_dict[new_pos] == "#":
            return current_pos
        else:
            return new_pos

for move in moves:
    if move.isdigit():
        steps = int(move)
        for i in range(steps):
            current_pos = get_next_pos(current_pos, facing)

    elif move == "R":
        facing = (facing + 1) % 4
    else:
        facing = (facing - 1) % 4


print(current_pos)
password = 1000 * current_pos[0] + 4*current_pos[1] + facing
print("Answer part one:", password)


# Part two
# cube layout:
#  BA
#  C
# ED
# F
