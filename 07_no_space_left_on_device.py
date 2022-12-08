from pathlib import PurePath
from pprint import pprint

import numpy as np

with open("data/07.txt", "r") as f:
    data = f.read().splitlines()

# part a
file_system = dict()
current_dir = PurePath("/") # keeps track of the current directory in the terminal
for command in data:
    if command.startswith("$ cd"):
        cd_dir = command.split(" ")[-1]
        if cd_dir == "/":
            current_dir = PurePath("/")
        elif cd_dir == "..":
            current_dir = current_dir.parent
        else:
            current_dir = current_dir / cd_dir
    elif command.startswith("$ ls"):
        continue
    else:
        info, entity_name = command.split(" ")
        file_path = current_dir / entity_name
        fs_dir = file_system
        for part in file_path.parts:
            if part not in fs_dir.keys():
                fs_dir[part] = dict()

            fs_dir["_type"] = "dir"
            fs_dir = fs_dir[part]

        if info.isdigit():
            fs_dir["_size"] = int(info)
            fs_dir["_type"] = "file"
        else:
            fs_dir["_type"] = "dir"

pprint(file_system)

global_list = list()
def calc_size(fs):
    if fs["_type"] == "dir":
        s = sum([calc_size(fs[part]) for part in fs.keys() if part[0] != "_"])
        global_list.append(s)
        return s
    elif "_size" in fs.keys():
        return fs["_size"]
    else:
        return 0


total_size = calc_size(file_system)
global_array = np.array(global_list)
print(np.sum(global_array[global_array < 100_000]))

# part b
space_needed = - (70_000_000 - total_size - 30_000_000)
print(global_array[global_array > space_needed].min())