input_path="input.txt"

with open(input_path, "r") as f:
    data = f.read().splitlines()

result = list()
chunksum=0
for row in data:
    if len(row)!=0:
        chunksum += int(row)
    else:
        result.append(chunksum)
        chunksum=0
        

print(sum(sorted(result)[-3:]))
