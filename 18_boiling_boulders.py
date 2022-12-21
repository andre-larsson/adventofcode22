from collections import defaultdict

import numpy as np

with open("data/18.txt") as f:
    data = f.readlines()

voxels= np.array([list(map(int, x.split(","))) for x in data])

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
gap_voxels = list()
num_gaps_found = defaultdict(int)

for line_d in [0,1,2]:
    plane_d = {0, 1, 2} - {line_d}
    plane_d = list(plane_d)
    planes = np.array([voxels[:, plane_d[0]], voxels[:, plane_d[1]]]).T
    # find planes with at least 2 points
    num_points = defaultdict(int)
    coord_dict = defaultdict(list)
    for i in range(len(planes)):
        num_points[tuple(planes[i])] += 1
        coord_dict[tuple(planes[i])].append(voxels[i][line_d])
    planes_to_check = [k for k, v in num_points.items() if v >= 2]

    for key in planes_to_check:
        d_coords = np.sort(coord_dict[key])
        gaps = (d_coords[1:] - d_coords[:-1]) == 2 # if distance of 2, there is a gap
        gap_coords = d_coords[:-1][gaps]+1 # get the gap coordinates
        for c in gap_coords:
            voxel = np.zeros(3)
            voxel[line_d] = c
            voxel[plane_d[0]] = key[0]
            voxel[plane_d[1]] = key[1]
            num_gaps_found[tuple(voxel)] += 1

air_bubbles = [k for k, v in num_gaps_found.items() if v >= 3]

print(air_bubbles)

exterior_sides = exposed_sides - len(air_bubbles)*6

print(exterior_sides)