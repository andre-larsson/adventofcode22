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
            map_dict[(i,j)] = c

p = re.compile('\d+|\D')
moves = p.findall(lines[-1])

all_coords = list(map_dict.keys())
init_pos = sorted(all_coords)[0]
facing = 0  # 0 = right, 1 = down, 2 = left, 3 = up

max_row = max([x[0] for x in all_coords])
max_col = max([x[1] for x in all_coords])


@cache
def get_next_pos(current_pos, facing):
    if facing == 0:  # right
        new_pos = (current_pos[0], current_pos[1] + 1)
        if new_pos not in all_coords:
            row = [x[1] for x in all_coords if x[0] == current_pos[0]]
            min_col = min(row)
            new_pos = (current_pos[0], min_col)
        if map_dict[new_pos] == "#":
            return current_pos
        else:
            return new_pos
    elif facing == 1:  # down
        new_pos = (current_pos[0] + 1, current_pos[1])
        if new_pos not in all_coords:
            col = [x[0] for x in all_coords if x[1] == current_pos[1]]
            min_row = min(col)
            new_pos = (min_row, current_pos[1])
        if map_dict[new_pos] == "#":
            return current_pos
        else:
            return new_pos
    elif facing == 2:  # left
        new_pos = (current_pos[0], current_pos[1] - 1)
        if new_pos not in all_coords:
            row = [x[1] for x in all_coords if x[0] == current_pos[0]]
            max_col = max(row)
            new_pos = (current_pos[0], max_col)
        if map_dict[new_pos] == "#":
            return current_pos
        else:
            return new_pos
    else: # up
        new_pos = (current_pos[0] - 1, current_pos[1])
        if new_pos not in all_coords:
            col = [x[0] for x in all_coords if x[1] == current_pos[1]]
            max_row = max(col)
            new_pos = (max_row, current_pos[1])
        if map_dict[new_pos] == "#":
            return current_pos
        else:
            return new_pos

def do_moves(current_pos, facing, moves):
    for move in moves:
        if move.isdigit():
            steps = int(move)
            for i in range(steps):
                current_pos = get_next_pos(current_pos, facing)

        elif move == "R":
            facing = (facing + 1) % 4
        else:
            facing = (facing - 1) % 4
    return current_pos, facing


current_pos_a, facing_a = do_moves(tuple(init_pos), 0, moves)
password = 1000 * (current_pos_a[0]+1) + 4*(current_pos_a[1]+1) + facing_a
print("Answer part one:", password)


# Part two
# cube layout:
#  BA
#  C
# ED
# F

# right, down, left, up
# https://www.geogebra.org/m/QAPeq2cw
side_connections = {
    ("A", 0) : ("D", 0, 2), # face, side, facing
    ("A", 1) : ("C", 0, 2),
    ("A", 2) : ("B", 0, 2),
    ("A", 3) : ("F", 1, 1),
    ("B", 0) : ("A", 2, 0),
    ("B", 1) : ("C", 3, 1),
    ("B", 2) : ("E", 2, 0),
    ("B", 3) : ("F", 2, 0),
    ("C", 0) : ("A", 1, 3),
    ("C", 1) : ("D", 3, 1),
    ("C", 2) : ("E", 3, 1),
    ("C", 3) : ("B", 1, 3),
    ("D", 0) : ("A", 0, 2),
    ("D", 1) : ("F", 0, 2),
    ("D", 2) : ("E", 0, 2),
    ("D", 3) : ("C", 1, 3),
    ("E", 0) : ("D", 2, 0),
    ("E", 1) : ("F", 3, 3),
    ("E", 2) : ("B", 2, 0),
    ("E", 3) : ("C", 2, 0),
    ("F", 0) : ("D", 1, 3),
    ("F", 1) : ("A", 3, 1),
    ("F", 2) : ("B", 3, 1),
    ("F", 3) : ("E", 1, 3),
}

# check consistency
for key in side_connections.keys():
    face, side, facing = side_connections[key]
    face2, side2, facing2 = side_connections[(face, side)]

    if face2 != key[0] or side2 != key[1]:
        print("Sides should be connected!:", key)


def get_cube_coords(pos):
    y_box = int(pos[0] / 50)
    x_box = int(pos[1] / 50)

    y = pos[0] % 50
    x = pos[1] % 50
    if y_box == 0 and x_box == 1:
        return "B", y, x
    elif y_box == 0 and x_box == 2:
        return "A", y, x
    elif y_box == 1 and x_box == 1:
        return "C", y, x
    elif y_box == 2 and x_box == 0:
        return "E", y, x
    elif y_box == 2 and x_box == 1:
        return "D", y, x
    elif y_box == 3 and x_box == 0:
        return "F", y, x
    else:
        print(x, y)
        return "?", y, x

# cube layout:
#  BA
#  C
# ED
# F

def cube_coords_to_map_coords(face, pos):
    if face == "B":
        upper_right = (0,50)
    elif face == "A":
        upper_right = (0,100)
    elif face == "C":
        upper_right = (50,50)
    elif face == "D":
        upper_right = (100,50)
    elif face == "E":
        upper_right = (100,0)
    else:
        upper_right = (150,0)
    return upper_right[0] + pos[0], upper_right[1] + pos[1]


@cache
def get_next_pos_cube(current_pos, facing):
    if facing == 0:  # right
        new_pos = (current_pos[0], current_pos[1] + 1)
        if new_pos not in all_coords:
            cube_side, cx, cy = get_cube_coords(current_pos)
            new_face, new_side, new_facing = side_connections[(cube_side, facing)]

            if new_side == 0: # right
                cx, cy = 49, cy
            elif new_side == 1: # down
                cx, cy = cy, 49
            elif new_side == 2: # left
                cx, cy = 0, cy
            else:
                cx, cy = cy, 0 # up

            new_pos = cube_coords_to_map_coords(new_face, (cx, cy))
        if map_dict[new_pos] == "#":
            return current_pos
        else:
            return new_pos
    elif facing == 1:  # down
        new_pos = (current_pos[0] + 1, current_pos[1])
        if new_pos not in all_coords:
            cube_side, cx, cy = get_cube_coords(current_pos)
            new_face, new_side, new_facing = side_connections[(cube_side, facing)]

            if new_side == 0: # right
                cx, cy = 49, cx
            elif new_side == 1: # down
                cx, cy = cx, 49
            elif new_side == 2: # left
                cx, cy = 0, cx
            else:
                cx, cy = cx, 0 # up

            new_pos = cube_coords_to_map_coords(new_face, (cx, cy))
        if map_dict[new_pos] == "#":
            return current_pos
        else:
            return new_pos
    elif facing == 2:  # left
        new_pos = (current_pos[0], current_pos[1] - 1)
        if new_pos not in all_coords:
            cube_side, cx, cy = get_cube_coords(current_pos)
            new_face, new_side, new_facing = side_connections[(cube_side, facing)]

            if new_side == 0: # right
                cx, cy = 49, cy
            elif new_side == 1: # down
                cx, cy = cy, 49
            elif new_side == 2: # left
                cx, cy = 0, cy
            else:
                cx, cy = cy, 0 # up

            new_pos = cube_coords_to_map_coords(new_face, (cx, cy))
        if map_dict[new_pos] == "#":
            return current_pos
        else:
            return new_pos
    else: # up
        new_pos = (current_pos[0] - 1, current_pos[1])

        if new_pos not in all_coords:
            cube_side, cx, cy = get_cube_coords(current_pos)
            new_face, new_side, new_facing = side_connections[(cube_side, facing)]

            if new_side == 0: # right
                cx, cy = 49, cx
            elif new_side == 1: # down
                cx, cy = cx, 49
            elif new_side == 2: # left
                cx, cy = 0, cx
            else:
                cx, cy = cx, 0 # up

            new_pos = cube_coords_to_map_coords(new_face, (cx, cy))

        if map_dict[new_pos] == "#":
            return current_pos
        else:
            return new_pos


def do_moves_cube(current_pos, facing, moves):
    for move in moves:
        if move.isdigit():
            steps = int(move)
            for i in range(steps):
                current_pos = get_next_pos_cube(current_pos, facing)
                pass

        elif move == "R":
            facing = (facing + 1) % 4
        else:
            facing = (facing - 1) % 4
    return current_pos, facing


final_pos_b, facing_b = do_moves_cube(tuple(init_pos), 0, moves)
password_b = 1000 * (final_pos_b[0]+1) + 4*(final_pos_b[1]+1) + facing

print(password_b)  # 50603 too high