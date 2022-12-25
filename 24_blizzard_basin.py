from copy import deepcopy
from functools import cache

import numpy as np

with open("data/24.txt") as f:
    lines = f.readlines()

move_dict = {"^" : (-1,0),
                "v" : (1,0),
                ">" : (0,1),
                "<" : (0,-1),}

blizzard_dict = dict()
init_grid = np.ones((len(lines),len(lines[0].strip())), dtype=bool)
start = (0,1)
end = (init_grid.shape[0]-1, init_grid.shape[1]-2)


for i, line in enumerate(lines):
    for j, e in enumerate(line):
        if e == "^" or e == "v" or e == "<" or e == ">":
            blizzard_dict[f"{i}_{j}"] = (e, i, j)
            init_grid[i, j] = False
        elif e == ".":
            init_grid[i,j] = False

def add_blizzards(blizzard_dict):
    grid = deepcopy(init_grid)
    for blizzard, state in blizzard_dict.items():
        direction, i, j = state
        grid[i, j] = True
    return grid



def blizzard_to_str(grid, blizzard_dict):
    grid_str = np.where(grid, "#", ".")
    for blizzard, state in blizzard_dict.items():
        direction, i, j = state
        if grid_str[i, j] == "." or grid_str[i, j] == "#":
            grid_str[i, j] = direction
        elif grid_str[i, j].isdigit():
            grid_str[i, j] = str(int(grid_str[i, j])+1)
        else:
            grid_str[i, j] = "2"

    rows = [ "".join(row) for row in grid_str]
    return "\n".join(rows)

def move_blizzard(grid, blizzard_dict):
    for blizzard, state in blizzard_dict.items():
        direction, i, j = state
        if direction == "^":
            new_pos = (i-1, j)
            if new_pos[0] < 1:
                new_pos = (grid.shape[0]-2, new_pos[1])
        elif direction == "v":
            new_pos = (i+1, j)
            if new_pos[0] >= grid.shape[0]-1:
                new_pos = (1, new_pos[1])
        elif direction == ">":
            new_pos = (i, j+1)
            if new_pos[1] >= grid.shape[1]-1:
                new_pos = (new_pos[0], 1)
        elif direction == "<":
            new_pos = (i, j-1)
            if new_pos[1] < 1:
                new_pos = (new_pos[0], grid.shape[1]-2)
        else: # should not happen
            new_pos = (i, j)
        blizzard_dict[blizzard] = (direction, new_pos[0], new_pos[1])

    grid = add_blizzards(blizzard_dict)

    return grid, blizzard_dict


def simulate_blizzard(grid, blizzard_dict, n=5):
    states = []
    states.append((deepcopy(grid), deepcopy(blizzard_dict)))
    # print(blizzard_to_str(grid, blizzard_dict))
    for i in range(n):
        # print("\ntime", i+1)
        grid, blizzard_dict = move_blizzard(grid, blizzard_dict)
        states.append((deepcopy(grid), deepcopy(blizzard_dict)))
        # print(blizzard_to_str(grid, blizzard_dict))
    return states

# blizzard_dict.clear()

max_time = 1000
states = simulate_blizzard(deepcopy(init_grid), deepcopy(blizzard_dict), max_time+1)

def get_moves(cur_pos, next_state):
    moves = []

    # down
    if cur_pos[0] < next_state.shape[0]-1 and not next_state[cur_pos[0] + 1, cur_pos[1]]:
        moves.append((cur_pos[0] + 1, cur_pos[1]))
    # right
    if cur_pos[1] < next_state.shape[1]-1 and not next_state[cur_pos[0], cur_pos[1] + 1]:
        moves.append((cur_pos[0], cur_pos[1] + 1))
    # up
    if cur_pos[0] >0 and not next_state[cur_pos[0] - 1, cur_pos[1]]:
        moves.append((cur_pos[0] - 1, cur_pos[1]))
    # left
    if cur_pos[1] >0 and not next_state[cur_pos[0], cur_pos[1] - 1]:
        moves.append((cur_pos[0], cur_pos[1] - 1))
    # wait
    if not next_state[cur_pos[0], cur_pos[1]]:
        moves.append(cur_pos)
    return moves


import sys
sys.setrecursionlimit(10000)

def adjacent(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1]) == 1

@cache
def reach_goal(current_pos, goal, time):
    global max_time
    if adjacent(current_pos, goal):
        max_time = min(max_time, time+1)
        return time+1

    if time > max_time:
        return 99999

    moves = get_moves(current_pos, states[time+1][0])
    if len(moves) == 0:
        return 99999

    return min([reach_goal(move, goal, time+1) for move in moves])

time_start0 = 0
time_end0 = reach_goal(start, end, time_start0)

print("Answer 1 (start-end):", time_end0)

# part 2
max_time = 1000
time_start1= reach_goal(end, start, time_end0)

print("(start-end-start):", time_start1)

max_time = 1000
time_end1= reach_goal(start, end, time_start1)

print("Answer 2 (start-end-start-end):", time_end1)