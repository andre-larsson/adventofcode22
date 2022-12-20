# load the data
from collections import defaultdict
from copy import deepcopy, copy
from pprint import pprint
from time import perf_counter

import numpy as np

with open("data/16.txt", "r") as f:
    lines = f.read().split("\n")

init_valve_dict = dict()
for line in lines:
    line = line.split(" ")
    flow_rate = int(line[4].split("=")[1].strip(";"))
    neighbors = [x.strip(",") for x in line[9:]]
    init_valve_dict[line[1]] = {"neighbors": neighbors,
                                "flow_rate": flow_rate}

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

def get_moves(valve_dict, start_pos, countdown):
    distances, previous = get_distances(valve_dict, start_pos)
    valve_scores = list()
    for valve, dist in distances.items():
        if dist+1 > countdown:
            continue

        flow_rate = valve_dict[valve]["flow_rate"]
        if flow_rate > 0:
            valve_scores.append((valve, dist, flow_rate))

    return valve_scores

def calculate_pressure1(valve_dict, current_valve, valve_is_open, countdown=30, total_ppm=0):
    if countdown <= 0:
        return 0

    valve_list = get_moves(valve_dict, current_valve, countdown)
    valve_list = [x for x in valve_list if not valve_is_open[x[0]]]


    total_pressure_list = list()

    for valve in valve_list:
        valve_name, dist, flow_rate = valve

        new_valve_is_open = valve_is_open.copy()
        new_valve_is_open[valve_name] = True

        total_pressure = calculate_pressure1(valve_dict, valve_name, new_valve_is_open, countdown-dist-1,
                                            total_ppm+flow_rate) + total_ppm * (dist+1)
        total_pressure_list.append(total_pressure)

    if len(total_pressure_list) > 0:
        return max(total_pressure_list)
    else:
        return countdown * total_ppm

# part a
valve_dict = deepcopy(init_valve_dict)
valve_is_open = defaultdict(lambda: False)
t0 = perf_counter()
total_pressure = calculate_pressure1(valve_dict, "AA", valve_is_open)
print(f"Total pressure: {total_pressure}")
print(f"Time: {perf_counter() - t0}")


class Agent:
    def __init__(self, current_valve = "AA"):
        self.current_valve = current_valve
        self.target_valve = None
        self.dist_to_target = 0
        self.opening_valve = False
        self.is_moving = False

    def update_location(self):
        if self.dist_to_target <= 0 and self.is_moving:
            self.current_valve = self.target_valve
            self.target_valve = None
            self.is_moving = False
            self.dist_to_target = 0
            self.opening_valve = True

    def set_target(self, target_valve, dist_to_target):
        self.target_valve = target_valve
        self.dist_to_target = dist_to_target
        self.is_moving = True

    def move_towards_target(self, steps=1):
        self.dist_to_target = max(self.dist_to_target - steps, 0)
        self.update_location()

    def __repr__(self):
        repr_str = vars(self)
        return str(repr_str)

def calculate_pressure2(valve_dict, a1, a2,
                        valve_is_open, countdown=26, total_ppm=0, history=[]):

    history = history.copy()
    history.append((deepcopy(a1), deepcopy(a2), total_ppm, countdown))

    if countdown <= 0:
        return 0, history

    new_total_ppm = total_ppm

    if a1.opening_valve:
        # a1 is opening a valve this turn
        new_total_ppm += valve_dict[a1.current_valve]["flow_rate"] # flow rate increases
        a1.opening_valve = False # reset opening valve
        valve_list1 = list() # no moves for a1
    elif a1.is_moving:
        a1.move_towards_target(1)
        valve_list1 = list()
    else:
        valve_list1 = get_moves(valve_dict, a1.current_valve, countdown)
        valve_list1 = [x for x in valve_list1 if not valve_is_open[x[0]]]

    if a2.opening_valve:
        new_total_ppm += valve_dict[a2.current_valve]["flow_rate"]
        a2.opening_valve = False
        valve_list2 = list()
    elif a2.is_moving:
        a2.move_towards_target(1)
        valve_list2 = list()
    else:
        valve_list2 = get_moves(valve_dict, a2.current_valve, countdown)
        valve_list2 = [x for x in valve_list2 if not valve_is_open[x[0]]]


    total_pressure_list = list()

    if len(valve_list1) == 0 and len(valve_list2) == 0:
        result = calculate_pressure2(valve_dict, deepcopy(a1), deepcopy(a2) , deepcopy(valve_is_open), countdown-1, new_total_ppm, history)
        return result[0] + total_ppm, result[1]
    elif len(valve_list2) == 0:
        # find new target for agent 1, loop through all possibilities
        for valve1 in valve_list1:
            valve_name, dist, flow_rate = valve1
            a1_new = deepcopy(a1)
            a1_new.set_target(valve_name, dist)
            a1_new.move_towards_target(1)
            new_valve_is_open = deepcopy(valve_is_open)
            new_valve_is_open[valve_name] = True

            result = calculate_pressure2(valve_dict, a1_new, deepcopy(a2), new_valve_is_open, countdown-1, new_total_ppm, history)
            total_pressure_list.append((result[0] + total_ppm, result[1]))
    elif len(valve_list1) == 0:
        # find new target for agent 2
        for valve2 in valve_list2:
            valve_name, dist, flow_rate = valve2
            a2_new = deepcopy(a2)
            a2_new.set_target(valve_name, dist)
            a2_new.move_towards_target(1)

            new_valve_is_open = deepcopy(valve_is_open)
            new_valve_is_open[valve_name] = True

            result = calculate_pressure2(valve_dict, deepcopy(a1), a2_new, new_valve_is_open, countdown-1, new_total_ppm, history)
            total_pressure_list.append((result[0] + total_ppm, result[1]))
    else:
        # find new target for both agents
        for i, valve1 in enumerate(valve_list1):
            for j, valve2 in enumerate(valve_list2):
                if i > j:
                    continue

                if i == j and (len(valve_list1) != 1 or len(valve_list2) != 1):
                    continue

                if i == j:
                    # same valve, only one agent can move
                    valve_name1, dist1, flow_rate1 = valve1

                    a1_new = deepcopy(a1)

                    a1_new.set_target(valve_name1, dist1)
                    a1_new.move_towards_target(1)

                    new_valve_is_open = deepcopy(valve_is_open)
                    new_valve_is_open[valve_name1] = True

                    result = calculate_pressure2(valve_dict, a1_new, deepcopy(a2), new_valve_is_open, countdown-1, new_total_ppm, history)

                    total_pressure_list.append((result[0] + total_ppm, result[1]))
                else:
                    valve_name1, dist1, flow_rate1 = valve1
                    valve_name2, dist2, flow_rate2 = valve2

                    a1_new = deepcopy(a1)
                    a2_new = deepcopy(a2)

                    a1_new.set_target(valve_name1, dist1)
                    a2_new.set_target(valve_name2, dist2)

                    a1_new.move_towards_target(1)
                    a2_new.move_towards_target(1)

                    new_valve_is_open = deepcopy(valve_is_open)
                    new_valve_is_open[valve_name1] = True
                    new_valve_is_open[valve_name2] = True

                    result = calculate_pressure2(valve_dict, a1_new, a2_new, new_valve_is_open, countdown-1, new_total_ppm, history)

                    total_pressure_list.append((result[0] + total_ppm, result[1]))

    if len(total_pressure_list) == 0:
        return total_ppm, history
    else:
        max_pressure = max(total_pressure_list, key=lambda x: x[0])
        for result in total_pressure_list:
            if result[0] == max_pressure[0]:
                return result

valve_dict = deepcopy(init_valve_dict)
valve_is_open = defaultdict(lambda: False)
t0 = perf_counter()
result = calculate_pressure2(valve_dict, Agent(), Agent(), valve_is_open, 26)
print(result)
print(f"Time: {perf_counter() - t0}")

for i, d in enumerate(result[1]):
    print(f"== Minute {i} ==")
    print(f"{d[0]}")
    print(f"{d[1]}")
    print(f"Total pressure/minute: {d[2]}")
    print(f"Countdown: {d[3]}")

print(f"Total pressure: {result}")
