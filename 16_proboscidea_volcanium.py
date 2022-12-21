from collections import defaultdict
from itertools import combinations
from copy import deepcopy
from pprint import pprint
from time import perf_counter
from joblib import Parallel, delayed

import numpy as np

# load the data

with open("data/16.txt", "r") as f:
    lines = f.read().split("\n")

init_valve_dict = dict()
for line in lines:
    line = line.split(" ")
    flow_rate = int(line[4].split("=")[1].strip(";"))
    neighbors = [x.strip(",") for x in line[9:]]
    init_valve_dict[line[1]] = {"neighbors": neighbors,
                                "flow_rate": flow_rate}

def get_distances(start_valve):
    """ Dijkstra's algorithm (again!)"""
    distances = defaultdict(lambda: np.inf)
    distances[start_valve] = 0

    vertices = list(init_valve_dict.keys())

    while len(vertices) > 0:
        min_vertex = min(vertices, key=lambda x: distances[x])

        # remove min_vertex from vertices
        vertices.remove(min_vertex)

        for neighbor in init_valve_dict[min_vertex]["neighbors"]:
            new_distance = distances[min_vertex] + 1
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance

    return distances

pprint(init_valve_dict)

# calculate the distances we need beforehand
valve_distances = dict()
for key, value in init_valve_dict.items():
    # valves with no flow_rate will not help us
    if value["flow_rate"] == 0 and key != "AA":
        continue
    valve_distances[key] = get_distances(key)
    for key2, value2 in valve_distances.items():
        if init_valve_dict[key2]["flow_rate"] == 0:
            valve_distances[key].pop(key2)


def get_moves(start_pos, countdown):
    distances = valve_distances[start_pos]
    valve_scores = list()
    for valve, dist in distances.items():
        if dist+1 > countdown:
            continue

        flow_rate = init_valve_dict[valve]["flow_rate"]
        if flow_rate > 0:
            valve_scores.append((valve, dist, flow_rate))

    return valve_scores

def calculate_pressure1(current_valve, opened_valves, countdown=30, total_ppm=0):
    if countdown <= 0:
        return 0, opened_valves

    valve_list = get_moves(current_valve, countdown)
    valve_list = [x for x in valve_list if not x[0] in opened_valves]


    total_pressure_list = list()

    for valve in valve_list:
        valve_name, dist, flow_rate = valve

        new_opened_valves = set(opened_valves)
        new_opened_valves.add(valve_name)

        result = calculate_pressure1(valve_name, frozenset(new_opened_valves), countdown-dist-1,
                                            total_ppm+flow_rate)

        total_pressure_list.append((result[0]+ total_ppm * (dist+1), result[1]))

    if len(total_pressure_list) > 0:
        return max(total_pressure_list, key = lambda x: x[0])
    else:
        return countdown * total_ppm, opened_valves

# part a
valve_dict = deepcopy(init_valve_dict)
opened_valves = frozenset()

t0 = perf_counter()
total_pressure, visited = calculate_pressure1("AA", opened_valves)
print(f"Total pressure: {total_pressure}")
print(f"Visited valves: {visited}")
print(f"Time: {perf_counter() - t0:.2f} s")


# part b

# if the elephant opens valves a,b,c, then human must try to open the other valves
# since the human and elephant act independently, we can add the pressures
# just have to check all combinations
valves_to_open = set(valve_distances.keys())
valves_to_open.remove("AA")
reserved_valves = list()

for n in range((len(valves_to_open) + 1)//2): # only need to check one diagonal
    reserved_valves += list(combinations(valves_to_open, n))

print(f"Number of combinations to check: {len(reserved_valves)}")

def worker(reserved_valve):
    valves_for_elephant = frozenset(reserved_valve)
    valves_for_human = frozenset(valves_to_open - valves_for_elephant)
    p1, v1 = calculate_pressure1("AA", valves_for_elephant, 26)
    p2, v2 = calculate_pressure1("AA", valves_for_human, 26)
    return p1 + p2

t0 = perf_counter()
result = Parallel(n_jobs=8)(delayed(worker)(x) for x in reserved_valves)

print(f"Best pressure: {max(result)}")
print(f"Time: {perf_counter() - t0:.2f} s") # ~ 1min on 8 core laptop
