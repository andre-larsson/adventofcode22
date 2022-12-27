from collections import defaultdict
from copy import deepcopy
import math
from time import perf_counter
from heapq import heapify, heappush, heappop


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

blizzard_height = init_grid.shape[0] - 2
blizzard_width = init_grid.shape[1] - 2

if blizzard_height == blizzard_width:
    blizzard_period = blizzard_height
else:
    gcd = math.gcd(blizzard_height, blizzard_width)
    blizzard_period = (blizzard_height * blizzard_width) // gcd

print(blizzard_height, blizzard_width)
# minimum time for when blizzard will repeat
print("Blizzard periodicity is:", blizzard_period)


for i, line in enumerate(lines):
    for j, e in enumerate(line):
        if e == "^" or e == "v" or e == "<" or e == ">":
            blizzard_dict[f"{i}_{j}"] = (e, i, j)
            init_grid[i, j] = False
        elif e == ".":
            init_grid[i,j] = False

def create_grid_with_blizzards(blizzard_dict):
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

    grid = create_grid_with_blizzards(blizzard_dict)

    return grid, blizzard_dict


def simulate_blizzard(grid, blizzard_dict, n=10):
    states = []
    states.append((deepcopy(grid), deepcopy(blizzard_dict)))
    # print(blizzard_to_str(grid, blizzard_dict))
    for i in range(n):
        # print("\ntime", i+1)
        grid, blizzard_dict = move_blizzard(grid, blizzard_dict)
        states.append((deepcopy(grid), deepcopy(blizzard_dict)))
        # print(blizzard_to_str(grid, blizzard_dict))
    return states


max_time = 1000
states = simulate_blizzard(deepcopy(init_grid), deepcopy(blizzard_dict), blizzard_period)

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


def a_star_search(start, goal, time=0):

    # heuristic is manhattan distance
    h = lambda x: abs(x[0] - goal[0]) + abs(x[1] - goal[1])

    start_node = (start[0], start[1], time)

    # note: score is time
    g_score = defaultdict(lambda: np.inf)
    g_score[start_node] = time

    f_score = defaultdict(lambda: np.inf)
    f_score[start_node] = h(start_node)

    open_set = [(f_score[start_node], start_node)]
    heapify(open_set)


    while open_set:
        _, current = heappop(open_set)
        if current[0:2] == goal:
            return g_score[current]

        for move in get_moves(current, states[int((g_score[current]+1) % blizzard_period)][0]):
            tentative_g_score = g_score[current] + 1
            move = (move[0], move[1], tentative_g_score)
            if tentative_g_score < g_score[move]:
                g_score[move] = tentative_g_score
                f_score[move] = tentative_g_score + h(move)
                heappush(open_set, (f_score[move], move))
    return np.inf

t0 = perf_counter()
time_start0 = a_star_search(start, end)
print("Answer part 1 (start-end):", time_start0)

time_start1 = a_star_search(end, start, time_start0)
print("(start-end-start):", time_start1)

time_end1 = a_star_search(start, end, time_start1)
print("Answer part 2 (start-end-start-end):", time_end1)
print(f"Total time: {perf_counter() - t0:.5f} s")