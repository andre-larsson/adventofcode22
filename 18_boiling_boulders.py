import numpy as np

with open("data/18.txt") as f:
    data = f.readlines()

voxels= np.array([list(map(lambda x: int(x)+1, x.split(","))) for x in data])

# add one to each dimension, to make sure there is air around it
# (for part b)
print(voxels)

# part a
def calc_num_connections(voxels):
    manh_matrix = np.zeros((voxels.shape[0], voxels.shape[0]))
    for i in range(len(voxels)):
        voxel = voxels[i]
        # connected if manhattan distance is 1
        manh = np.sum(np.abs(voxels-voxel), axis=1)
        manh_matrix[i, :] = manh
    return np.sum(manh_matrix==1)

exposed_sides = 6*len(voxels) - calc_num_connections(voxels)
print(exposed_sides)

# part b

cube_bounds = np.array([np.min(voxels, axis=0)-1, np.max(voxels, axis=0)+1]).T
print(cube_bounds)
cube_volume = np.prod(cube_bounds[:,1]-cube_bounds[:,0])
print(f"Volume: {cube_volume}")

lava_voxels = frozenset([tuple(x) for x in voxels])
def get_new_neighbours(voxel, filled_voxels):
    result = []
    if voxel[0] > cube_bounds[0, 0]:
        result.append(voxel + np.array([-1, 0, 0]))
    if voxel[1] > cube_bounds[1, 0]:
        result.append(voxel + np.array([0, -1, 0]))
    if voxel[2] > cube_bounds[2, 0]:
        result.append(voxel + np.array([0, 0, -1]))
    if voxel[0] < cube_bounds[0, 1]:
        result.append(voxel + np.array([1, 0, 0]))
    if voxel[1] < cube_bounds[1, 1]:
        result.append(voxel + np.array([0, 1, 0]))
    if voxel[2] < cube_bounds[2, 1]:
        result.append(voxel + np.array([0, 0, 1]))

    neighbours_set = [tuple(x) for x in result if tuple(x) not in filled_voxels]
    return neighbours_set

filled_voxels = set()

# voxels_to_check is a set of tuples
# set means impossible to list the same voxel twice
voxels_to_check = set([tuple(cube_bounds[:, 0])])
num_exterior = 0
while len(voxels_to_check) > 0:
    voxel = voxels_to_check.pop()

    filled_voxels.add(voxel)
    neighbours = get_new_neighbours(voxel, frozenset(filled_voxels))

    for neighbour in neighbours:
        # if neighbour is lava, we have found an exterior side
        if neighbour in lava_voxels:
            num_exterior += 1
            continue
        if neighbour not in filled_voxels:
            voxels_to_check.add(neighbour)

print(num_exterior)