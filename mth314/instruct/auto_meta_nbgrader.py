# add nbgrader metadata

import json
import numpy as np
import sys

def is_command(line):
  if "ANSWER" in process_comment(line)[0] or "AMSWER" in process_comment(line)[1]:
    return True
  else:
    return False

def process_comment(line):
  command = line.replace("#","")
  command = command.strip()
  # if command[:3] == "AGA":
  return [i.strip() for i in command.split()]

ASSIGNMENT = sys.argv[1]
ind = ASSIGNMENT.index("INST")
ext = ASSIGNMENT.index(".ipynb")
# NEW_ASSIGNMENT = ASSIGNMENT[:ind] + "STUDENT" + ASSIGNMENT[ext:]

with open(ASSIGNMENT, 'r+', encoding="utf-8") as file:
  data = json.load(file)


print(data)

for cell in data['cells']:
  if is_command(cell['source'][0]) == True:
    cell_type = process_comment(cell['source'])
    if cell_type[0] == "AA":
      cell["metadata"]["nbgrader"]["grade"] = False
