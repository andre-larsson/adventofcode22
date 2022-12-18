# load the data
with open("data/16.txt", "r") as f:
    lines = f.read().split("\n")

valve_dict = dict()
for line in lines:
    line = line.split(" ")
    valve_dict[line[1]] = {"connections": line[9:],
                           "flow_rate": 0}

# idea: need to calculate shortest path to each valve from current?
# then total eventual pressure
# then go to valve with highest total eventual pressure?