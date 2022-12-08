with open("data/06.txt", "r") as f:
    data = f.read()
# part a
for i in range(len(data)-4):
    if len(set(data[i:i+4])) ==4:
        print(data[i:i+4])
        print(i+4)
        break

# part b
for i in range(len(data)-14):
    if len(set(data[i:i+14])) ==14:
        print(data[i:i+14])
        print(i+14)
        break