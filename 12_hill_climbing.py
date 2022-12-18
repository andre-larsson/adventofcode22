import string
from time import perf_counter

from joblib import Parallel, delayed

import numpy as np

# load the data
with open("data/12.txt", "r") as f:
    data = f.read().splitlines()

# initialize map, and start/end coordinates
height_table = {e: i for i, e in enumerate(string.ascii_lowercase)}
height_table["S"] = height_table["a"]
height_table["E"] = height_table["z"]
s_coord = np.array([0, 0])
e_coord = np.array([0, 0])
a_coords = list() # coordinates of all a's

hill_map = np.zeros((len(data), len(data[0])))
for row_i, row in enumerate(data):
    for col_i, col in enumerate(row):
        if col == "S":
            s_coord = np.array([row_i, col_i])
        elif col == "E":
            e_coord = np.array([row_i, col_i])
        elif col =="a":
            a_coords.append([row_i, col_i])

        hill_map[row_i, col_i] = height_table[col]


direction_table = {"<": np.array([0, -1]), ">": np.array([0, 1]), "^": np.array([-1, 0]), "v": np.array([1, 0])}

def move_is_possible(coord, new_coord):

    if new_coord[0] < 0 or new_coord[0] >= hill_map.shape[0] or \
        new_coord[1] < 0 or new_coord[1] >= hill_map.shape[1]:
        return False

    return (hill_map[new_coord[0], new_coord[1]]) <= hill_map[coord[0], coord[1]]+1

def get_possible_moves(coord):
    possible_moves = []
    for direction, direction_coord in direction_table.items():
        new_coord = coord + direction_coord
        if move_is_possible(coord, new_coord):
            possible_moves.append(direction_coord)
    return possible_moves


def get_distance(coord):
    """ Dijkstra's algorithm """
    distances = np.full_like(hill_map, np.inf)
    distances[coord[0], coord[1]] = 0
    prev_shortest = dict()

    vertices = np.zeros((hill_map.shape[0]*hill_map.shape[1],2), dtype=int)
    vertices[:, 0] = np.repeat(np.arange(hill_map.shape[0]), hill_map.shape[1])
    vertices[:, 1] = np.tile(np.arange(hill_map.shape[1]), hill_map.shape[0])

    while len(vertices) > 0:
        min_vertex = vertices[np.argmin(distances[vertices[:,0], vertices[:,1]])]

        if min_vertex[0] == e_coord[0] and min_vertex[1] == e_coord[1]:
            break

        vertices = vertices[~np.all(vertices == min_vertex, axis=1)]

        for direction_coord in get_possible_moves(min_vertex):
            new_vertex = min_vertex + direction_coord
            new_distance = distances[min_vertex[0], min_vertex[1]] + 1
            if new_distance < distances[new_vertex[0], new_vertex[1]]:
                distances[new_vertex[0], new_vertex[1]] = new_distance
                prev_shortest[tuple(new_vertex)] = tuple(min_vertex)
    return distances[e_coord[0], e_coord[1]]

# part a

print(get_distance(s_coord))

# part b
# multiprocessing to speed up
t0 = perf_counter()
result = Parallel(n_jobs=32)(delayed(get_distance)(a) for a in a_coords)
print(f"Time: {perf_counter()-t0:.2f} s")
print(np.min(result))
