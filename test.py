import os
import random

directory_path = 'column_files/'

files = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]

data = []
sample = []

for file_name in files:
    file_path = os.path.join(directory_path, file_name)
    with open(file_path, 'r') as file:
        lines = file.readlines()
        num_of_zeroes = 0
        # for line in lines[1:]:
        #     i = int(line.strip())
        #     if i != 0:
        #         break
        #     num_of_zeroes += 1
        # print(num_of_zeroes)
        sample.append(int(lines[5638].strip()))
print(min(sample))
print(max(sample))
print(random.randint(min(sample), max(sample)))