import numpy as np
import sys

def isComment(line):
    if "##" in line:
        return True
    else:
        return False

ASSIGNMENT = sys.argv[1]
ind = ASSIGNMENT.index("INST")
ext = ASSIGNMENT.index(".ipynb")
NEW_ASSIGNMENT = ASSIGNMENT[:ind] + "STUDENT" + ASSIGNMENT[ext:]

with open(ASSIGNMENT, 'r+', encoding="utf-8") as file:
    lines = file.readlines()

new_lines = []

LIMIT = len(lines)

i = 0

while i < LIMIT:
    if '"source"' in lines[i]:
        # if the first line of the source cell is ANSWER
        if isComment(lines[i+1]) and ("ANSWER" in lines[i+1] or "AMSWER" in lines[i+1]):
            # delete the first bracket of the cell
            del new_lines[-1]
            # temp variable to hold the lines after the pointer
            temp = lines[i+1:]
            # find the nearest ending bracket and add one (basically skipping the entire cell)
            i = i + temp.index("  },\n") + 1
    elif isComment(lines[i]) and ("ANSWER" in lines[i] or "AMSWER" in lines[i]):
        i += 1
        for temp_index, temp_line in enumerate(lines[i:]):
            if "ANSWER" in temp_line or "AMSWER" in temp_line:
                i = i + temp_index + 1
                # print(lines[i])
                break

    new_lines.append(lines[i])
    i += 1

# final answer check
for line in new_lines:
    if "ANSWER" in line or "AMSWER" in line:
        print("WARNING! Some answer content may remain in the file. Please double check file contents before administering to students.")
        break

with open(NEW_ASSIGNMENT, 'w+', encoding="utf-8") as f:
    for l in new_lines:
        f.write(l)