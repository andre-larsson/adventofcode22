import re
from pprint import pprint

with open("data/19.txt") as f:
    lines = f.readlines()

class BluePrint():
    def __init__(self, id: str, ore_cost: int, clay_cost: int, obs_cost: tuple, geode_cost:tuple):
        self.id = id
        self.ore_cost = ore_cost # ore
        self.clay_cost = clay_cost # ore
        self.obs_cost = obs_cost # ore, clay
        self.geode_cost = geode_cost # ore, obsidian

    def __repr__(self):
        return f"{self.id}: {self.ore_cost}, {self.clay_cost}, {self.obs_cost}, {self.geode_cost}"


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

        self.planned_production = [1,0,0,0]

        if time is None:
            self.time = 0
        else:
            self.time = time

        self.blueprint = blueprint

    def buy_ore_robot(self):
        if self.resources[0] >= self.blueprint.ore_cost:
            self.resources[0] -= self.blueprint.ore_cost
            self.planned_production[0] += 1
            return True
        else:
            return False

    def buy_clay_robot(self):
        if self.resources[0] >= self.blueprint.clay_cost:
            self.resources[0] -= self.blueprint.clay_cost
            self.planned_production[1] += 1
            return True
        else:
            return False

    def buy_obs_robot(self):
        if self.resources[0] >= self.blueprint.obs_cost[0] and self.resources[1] >= self.blueprint.obs_cost[1]:
            self.resources[0] -= self.blueprint.obs_cost[0]
            self.resources[1] -= self.blueprint.obs_cost[1]
            self.planned_production[2] += 1
            return True
        else:
            return False

    def buy_geode_robot(self):
        if self.resources[0] >= self.blueprint.geode_cost[0] and self.resources[2] >= self.blueprint.geode_cost[1]:
            self.resources[0] -= self.blueprint.geode_cost[0]
            self.resources[2] -= self.blueprint.geode_cost[1]
            self.planned_production[3] += 1
            return True
        else:
            return False

    def build_robots(self, order: tuple):
        """Build the robots specified by the tuple, return True if miner has all robots."""
        has_robots = True
        if order[0] > self.production[0]:
            has_robots = self.buy_ore_robot() and has_robots
        if order[1] > self.production[1]:
            has_robots = self.buy_clay_robot() and has_robots
        if order[2] > self.production[2]:
            has_robots = self.buy_obs_robot() and has_robots
        if order[3] > self.production[3]:
            has_robots = self.buy_geode_robot() and has_robots
        return has_robots

    def mine(self):
        self.resources[0] += self.production[0]
        self.resources[1] += self.production[1]
        self.resources[2] += self.production[2]
        self.resources[3] += self.production[3]
        self.time += 1
        # update production
        self.production = list(self.planned_production)


    def __repr__(self):
        return f"Blueprint: {self.blueprint.id}, time: {self.time}, " \
               f"resources: {self.resources}, production: {self.production}"


# read all blueprints
blueprints = list()
for line in lines:
    digits = re.findall(r"\d+", line)
    blueprints.append(BluePrint(digits[0], int(digits[1]), int(digits[2]),
                                (int(digits[3]), int(digits[4])), # obs cost
                                (int(digits[5]), int(digits[6])))) # geode cost


def build_robots(miner):
    while miner.buy_geode_robot():
        pass

    while miner.buy_obs_robot():
        pass

    while miner.buy_clay_robot():
        pass

    while miner.buy_ore_robot():
        pass

    return miner


build_order = [(1,0,0,0),
                (1,1,0,0),
                (1,2,0,0),
                (1,3,1,0),
                (1,4,1,0),
                (1,4,2,0),
                (1,4,2,1),
                (1,4,2,2),
                (1,4,2,3),
                (1,4,2,4)]


max_production = (5,4,4,3)
def generate_build_orders(current_build_order, all_build_orders):
    """Generate all possible build orders"""

    if all([current_build_order[-1][i] == max_production[i] for i in range(4)]):
        all_build_orders.append(current_build_order)
        return current_build_order, all_build_orders

    for i in range(4):
        if current_build_order[-1][i] >= max_production[i]:
            continue

        # cannot build without clay
        if i == 2 and current_build_order[-1][1]<=1:
            continue

        # cannot build without obsidian
        if i == 3 and current_build_order[-1][2]<=1:
            continue

        new_build_orders = list(current_build_order)
        new_build_orders.append(list(current_build_order[-1]))
        new_build_orders[-1][i] += 1
        new_build_orders, all_build_orders = generate_build_orders(new_build_orders,
                                                                   all_build_orders)
    return current_build_order, all_build_orders


_, all_build_orders = generate_build_orders([[1,0,0,0]], [])

print(len(all_build_orders))


def simulate_miner(blueprint, build_order):
    miner = MiningOperation(blueprint)
    build_order_i = 0
    num_build_orders = len(build_order)
    for i in range(24):
        while build_order_i < num_build_orders and miner.build_robots(build_order[build_order_i]):
            build_order_i += 1
        miner.mine()
    return miner.resources[-1], miner.production


print(simulate_miner(blueprints[0], all_build_orders[0]))

def find_optimal_build(blueprints, build_orders):
    best_geodes = list()
    final_productions = list()
    for blueprint in blueprints:
        best_geode = 0
        final_production = None
        for build_order in build_orders:
            geodes, fp = simulate_miner(blueprint, build_order)
            if geodes > best_geode:
                best_geode = geodes
                final_production = fp

        best_geodes.append(best_geode)
        final_productions.append(final_production)

    return best_geodes, final_productions


best_geodes, final_productions = find_optimal_build(blueprints, all_build_orders)

for i, b in enumerate(final_productions):
    print(f"{i+1}: {best_geodes}, {b}")