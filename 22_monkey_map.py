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
init_facing = 0  # 0 = right, 1 = down, 2 = left, 3 = up

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
# https://www.geogebra.org/m/QAPeq2cw, pattern 9
side_connections = {
    ("A", 0) : ("D", lambda x: (149 - x[0], 99), 2), # face, adjacent_pixel, new_facing
    ("A", 1) : ("C", lambda x: (x[1] - 50 , 99), 2),
    ("A", 2) : ("B", lambda x: (x[0] , x[1]-1), 2),
    ("A", 3) : ("F", lambda x: (199 , -100+x[1]), 3),
    ("B", 0) : ("A", lambda x: (x[0] , x[1]+1), 0),
    ("B", 1) : ("C", lambda x: (x[0]+1 , x[1]), 1),
    ("B", 2) : ("E", lambda x: (149-x[0] , 0), 0),
    ("B", 3) : ("F", lambda x: (100+x[1] , 0), 0),
    ("C", 0) : ("A", lambda x: (49, 50+x[0]), 3),
    ("C", 1) : ("D", lambda x: (x[0]+1 , x[1]), 1),
    ("C", 2) : ("E", lambda x: (100 , -50+x[0]), 1),
    ("C", 3) : ("B", lambda x: (x[0]-1 , x[1]), 3),
    ("D", 0) : ("A", lambda x: (149-x[0], 149), 2),
    ("D", 1) : ("F", lambda x: (100+x[1] ,49 ), 2),
    ("D", 2) : ("E", lambda x: (x[0] , x[1]-1), 2),
    ("D", 3) : ("C", lambda x: (x[0]-1 , x[1]), 3),
    ("E", 0) : ("D", lambda x: (x[0] , x[1]+1), 0),
    ("E", 1) : ("F", lambda x: (x[0]+1 , x[1]), 1),
    ("E", 2) : ("B", lambda x: (149-x[0] ,50 ), 0),
    ("E", 3) : ("C", lambda x: (50+x[1] ,50), 0),
    ("F", 0) : ("D", lambda x: (149 , -100+x[0]), 3),
    ("F", 1) : ("A", lambda x: (0 , 100+x[1]), 1),
    ("F", 2) : ("B", lambda x: (0 ,-100+x[0] ), 1),
    ("F", 3) : ("E", lambda x: (x[0]-1 , x[1]), 3),
}


facing_to_char = {0: ">" , 1: "v", 2: "<", 3: "^"}

def map_to_str(current_pos, facing):
    s = ""
    for i in range(max_row+1):
        for j in range(max_col+1):
            if (i,j) == current_pos:
                s += str(facing_to_char[facing])
            elif (i,j) in map_dict.keys():
                s += map_dict[(i,j)]
            else:
                s += " "
        s += "\n"
    return s



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
        print(y, x)
        return "?", y, x

# cube layout:
#  BA
#  C
# ED
# F

@cache
def get_next_pos_cube(current_pos, facing, all_empty=False):

    new_facing = facing

    if facing == 0:  # right
        new_pos = (current_pos[0], current_pos[1] + 1)
    elif facing == 1:  # down
        new_pos = (current_pos[0] + 1, current_pos[1])
    elif facing == 2:  # left
        new_pos = (current_pos[0], current_pos[1] - 1)
    else: # up
        new_pos = (current_pos[0] - 1, current_pos[1])

    if new_pos not in all_coords:
        cube_side, _cx, _cy = get_cube_coords(current_pos)
        new_face, f_adjacent_pixel, new_facing = side_connections[(cube_side, facing)]
        new_pos = f_adjacent_pixel(current_pos)
        pass

    if new_pos not in all_coords:
        pass

    if map_dict[new_pos] == "#" or all_empty:
        return current_pos, facing
    else:
        return new_pos, new_facing


def do_moves_cube(current_pos, facing, moves, verbose=False):
    for move in moves:

        if verbose:
            print("move", move)
            print(current_pos)

        if move.isdigit():
            steps = int(move)
            for i in range(steps):
                current_pos, facing = get_next_pos_cube(current_pos, facing)

                if verbose:
                    print(i, current_pos)

        elif move == "R":
            facing = (facing + 1) % 4
        else:
            facing = (facing - 1) % 4

        if verbose:
            print(map_to_str(current_pos, facing))

    return current_pos, facing


def test_cube(pos, dir, verbose=True):
    """
    test cube topology
    if we start moving 200 steps in any direction, we should end up where we started
    in an empty grid
    """

    current_pos = tuple(pos)
    facing = dir
    if verbose:
        print(pos, facing)
    for i in range(200):
        current_pos, facing = get_next_pos_cube(current_pos, facing, all_empty=True)
        if verbose:
            print(i, current_pos, facing)

    return current_pos == pos and facing == dir


### DEBUGGING
print("Test topology, all should be True.")
for pos in [(0,50), (0, 100),
            (50, 50),
            (100, 0), (100, 50),
            (150, 0)]:  # start at topright corner of each face
    print("Face:", get_cube_coords(pos))
    for i in range(4): # test all directions
        passed_test = test_cube(pos, i, False)
        print(i, passed_test)
        if not passed_test:
            test_cube(pos, i, True)


# print(map_to_str(init_pos, 0))
final_pos_b, facing_b = do_moves_cube(tuple(init_pos), 0, moves)
password_b = 1000 * (final_pos_b[0]+1) + 4*(final_pos_b[1]+1) + facing_b

print("Answer part two:", password_b)
