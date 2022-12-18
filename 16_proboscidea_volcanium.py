# load the data
from collections import defaultdict
from copy import deepcopy
from pprint import pprint

import numpy as np

with open("data/16.txt", "r") as f:
    lines = f.read().split("\n")

init_valve_dict = dict()
for line in lines:
    line = line.split(" ")
    flow_rate = int(line[4].split("=")[1].strip(";"))
    neighbors = [x.strip(",") for x in line[9:]]
    init_valve_dict[line[1]] = {"neighbors": neighbors,
                                "flow_rate": flow_rate,
                                "open": False}

def get_distances(valve_dict, start_valve):
    """ Dijkstra's algorithm (again!)"""
    distances = defaultdict(lambda: np.inf)
    previous = defaultdict(lambda: None)
    distances[start_valve] = 0

    vertices = list(valve_dict.keys())

    while len(vertices) > 0:
        min_vertex = min(vertices, key=lambda x: distances[x])

        # remove min_vertex from vertices
        vertices.remove(min_vertex)

        for neighbor in valve_dict[min_vertex]["neighbors"]:
            new_distance = distances[min_vertex] + 1
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                previous[neighbor] = min_vertex

    return distances, previous

pprint(init_valve_dict)

def get_best_move(valve_dict, start_pos, countdown):
    distances, previous = get_distances(valve_dict, start_pos)
    valve_scores = list()
    for valve, dist in distances.items():
        if valve_dict[valve]["open"]:
            continue

        # calculate total eventual pressure (TEP) if
        # we go to a valve and open it
        flow_rate = valve_dict[valve]["flow_rate"]
        TEP = (countdown - dist-1) * flow_rate
        valve_scores.append((valve, TEP, dist+1, flow_rate))

    # sort by TEP, then by distance
    valve_scores.sort(key=lambda x: (x[1], x[2]), reverse=True)
    return valve_scores

tp_list = list()

def calculate_pressure(valve_dict, current_valve, countdown, total_ppm):

    if countdown <= 0:
        return 0

    valve_scores = get_best_move(valve_dict, current_valve, countdown)
    for valve_score in valve_scores:
        best_valve, TEP, dist, flow_rate = valve_score

        if best_valve is not None:
            valve_dict[best_valve]["open"] = True
            add_pressure = total_ppm * dist
            total_pressure = calculate_pressure(valve_dict, best_valve, countdown-dist, total_ppm+flow_rate)\
                             + add_pressure
            tp_list.append(total_pressure)
            return total_pressure

        else:
            return 0

valve_dict = deepcopy(init_valve_dict)
best_valve = "AA"
total_pressure = calculate_pressure(valve_dict, best_valve, 30, 0)
print(f"Total pressure: {total_pressure}")
print(f"Max pressure: {tp_list}")