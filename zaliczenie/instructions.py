from typing import TextIO

file = "instructions.txt"
instructions = []

with open(file, 'r') as f:
    lines = f.readlines()
    for line in lines:
        if not (line.startswith("#")):
            instructions.append(line)
        # print(instructions) #this is for troubleshooting
