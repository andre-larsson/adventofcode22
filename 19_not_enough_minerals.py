import re
from copy import deepcopy
from time import perf_counter

from joblib import Parallel, delayed

with open("data/19.txt") as f:
    lines = f.readlines()

class BluePrint():
    def __init__(self, id: str, ore_cost: int, clay_cost: int, obs_cost: tuple, geode_cost:tuple):
        self.id = id
        self.ore_cost = ore_cost # ore
        self.clay_cost = clay_cost # ore
        self.obs_cost = obs_cost # ore, clay
        self.geode_cost = geode_cost # ore, obsidian
        self.max_costs = (max(ore_cost, clay_cost, obs_cost[0], obs_cost[0]), # ore
                          obs_cost[1], # clay
                          geode_cost[1], # obsidian
                        0)  # geode

    def __repr__(self):
        return f"{self.id}: {self.ore_cost}, {self.clay_cost}, {self.obs_cost}, {self.geode_cost}"


# read all blueprints
blueprints = list()
for line in lines:
    digits = re.findall(r"\d+", line)
    blueprints.append(BluePrint(digits[0], int(digits[1]), int(digits[2]),
                                (int(digits[3]), int(digits[4])), # obs cost
                                (int(digits[5]), int(digits[6])))) # geode cost

class MiningOperation():
    def __init__(self, blueprint: BluePrint, resources: list = None, production: list = None, time: int = None):

        if resources is None:
            self.resources = [0,0,0,0] # ore, clay, obsidian, geodes
        else:
            self.resources = resources

        if production is None:
            self.production = [1,0,0,0]
        else:
            self.production = production

        # self.planned_production = [1,0,0,0]

        if time is None:
            self.time = 0
        else:
            self.time = time

        self.blueprint = blueprint
        self.max_costs = list(blueprint.max_costs)

    def from_tuple(self, t):
        self.__init__(self.blueprint, t[:4], t[4:8])
        return self

    def to_tuple(self):
        return tuple(self.resources + self.production + [self.time])


    def can_afford_ore(self):
        return self.resources[0] >= self.blueprint.ore_cost

    def build_ore_robot(self):
        self.resources[0] -= self.blueprint.ore_cost
        self.production[0] += 1

    def can_afford_clay(self):
        return self.resources[0] >= self.blueprint.clay_cost

    def build_clay_robot(self):
        self.resources[0] -= self.blueprint.clay_cost
        self.production[1] += 1

    def can_afford_obs(self):
        return self.resources[0] >= self.blueprint.obs_cost[0] and self.resources[1] >= self.blueprint.obs_cost[1]

    def build_obs_robot(self):
        self.resources[0] -= self.blueprint.obs_cost[0]
        self.resources[1] -= self.blueprint.obs_cost[1]
        self.production[2] += 1

    def can_afford_geode(self):
        return self.resources[0] >= self.blueprint.geode_cost[0] and self.resources[2] >= self.blueprint.geode_cost[1]

    def build_geode_robot(self):
        self.resources[0] -= self.blueprint.geode_cost[0]
        self.resources[2] -= self.blueprint.geode_cost[1]
        self.production[3] += 1

    def mine(self):
        self.resources[0] += self.production[0]
        self.resources[1] += self.production[1]
        self.resources[2] += self.production[2]
        self.resources[3] += self.production[3]
        self.time += 1

    def __repr__(self):
        return f"Blueprint: {self.blueprint.id}, time: {self.time}, " \
               f"resources: {self.resources}, production: {self.production}"


# best_geodes, final_productions = find_optimal_build(blueprints, all_build_orders)

# increase recursion limit
import sys
sys.setrecursionlimit(100000)

result_dict = dict()

def calc_geodes(miner, max_time=24):

    # check if we have already calculated this
    if miner.to_tuple() in result_dict:
        return result_dict[miner.to_tuple()]

    if miner.time >= max_time:
        result_dict[miner.to_tuple()] = miner.resources[-1]
        return miner.resources[-1]

    # if we can build a geode robot, always build it
    if miner.can_afford_geode():
        new_miner = deepcopy(miner)
        new_miner.mine()
        new_miner.build_geode_robot()
        return calc_geodes(new_miner, max_time)

    # test all of the other options

    possible_miner_states = []

    if miner.can_afford_ore() and miner.production[0] <= miner.max_costs[0]:
        new_miner = deepcopy(miner)
        new_miner.mine()
        new_miner.build_ore_robot()
        possible_miner_states.append(new_miner)
    if miner.can_afford_clay() and miner.production[1] <= miner.max_costs[1]:
        new_miner = deepcopy(miner)
        new_miner.mine()
        new_miner.build_clay_robot()
        possible_miner_states.append(new_miner)
    if miner.can_afford_obs() and miner.production[2] <= miner.max_costs[2]:
        new_miner = deepcopy(miner)
        new_miner.mine()
        new_miner.build_obs_robot()
        possible_miner_states.append(new_miner)
    if (miner.resources[0] < miner.max_costs[0] and miner.production[0] > 0) or \
        (miner.resources[1] < miner.max_costs[1] and miner.production[1] > 0) or \
        (miner.resources[2] < miner.max_costs[2] and miner.production[2] > 0):
        new_miner = deepcopy(miner)
        new_miner.mine()
        possible_miner_states.append(new_miner)


    if len(possible_miner_states) == 0:
        # result_dict[miner.to_tuple()] = miner.resources[-1]
        pass
        return miner.resources[-1]

    result = max([calc_geodes(miner, max_time) for miner in possible_miner_states])
    result_dict[miner.to_tuple()] = result

    return result


print("Starting calculations (part a)")
t0 = perf_counter() # start timer

result_a = Parallel(n_jobs=32)(delayed(calc_geodes)(MiningOperation(blueprint), 24) for blueprint in blueprints)

print(f"Total time: {(perf_counter() - t0)/60:.2f} minutes")
print(f"Answers: {result_a}")

sum_ql = sum([(i+1)*x for i, x in enumerate(result_a)])

print(f"Sum QL (part a): {sum_ql}")


print("Starting calculations (part b)")
t0 = perf_counter() # start timer
result = Parallel(n_jobs=8)(delayed(calc_geodes)(MiningOperation(blueprint), 32) for blueprint in blueprints[:3])

print(f"Total time: {(perf_counter() - t0)/60:.2f} minutes")

print(f"Answers: {result}")
mult = result[0]*result[1]*result[2]
print(f"Mult (part b): {mult}")