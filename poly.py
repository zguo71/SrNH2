import re

input_file = "poly"
output_file = "pi1_fit_6"



result = []

with open(input_file, "r") as f:
    for line in f:
        parts = line.strip().split()
        print(parts)
        coeff = float(parts[-1])
        row = [0,0,0,0,0,0]
        for part in parts[:-1]:
            print(part)
            coord = int(part[1])
            if len(part) > 2:
                row[coord - 1] = int(part[3:])
            else:
                row[coord - 1] = 1
        print(row)
        result.append(row + [coeff])
        print()

# save the results
with open(output_file, "w") as f:
    for row in result:
        f.write(" ".join(f"{x:3d}" for x in row[:-1]) + f"   {row[-1]: .8f}\n")

