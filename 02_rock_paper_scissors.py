import pandas as pd

points_dict = {
    "A": {"X": 1+3,
          "Y": 2+6,
          "Z": 3},
    "B": {"X": 1,
          "Y": 5,
          "Z": 9},
    "C": {"X": 7,
          "Y": 2,
          "Z": 6}
}

points_dict2 = {
    "A": {"X": 0+3,
          "Y": 3+1,
          "Z": 6+2},
    "B": {"X": 0+1,
          "Y": 3+2,
          "Z": 6+3},
    "C": {"X": 0+2,
          "Y": 3+3,
          "Z": 6+1}
}


rps_strategy = pd.read_csv("data/02.txt", delimiter=" ", header=None)

# 2a
scores = rps_strategy.apply(lambda x: points_dict[x.iloc[0]][x.iloc[1]], axis=1)
print(scores.sum())

# 2b
scores = rps_strategy.apply(lambda x: points_dict2[x.iloc[0]][x.iloc[1]], axis=1)
print(scores.sum())