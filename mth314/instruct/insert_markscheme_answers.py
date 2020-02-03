import json
import sys

ASSIGNMENT = sys.argv[1]
ind = ASSIGNMENT.index("INST")
ext = ASSIGNMENT.index(".ipynb")
NEW_ASSIGNMENT = ASSIGNMENT[:ind] + "STUDENT" + ASSIGNMENT[ext:]

with open(ASSIGNMENT, 'r+', encoding="utf-8") as file:
	notebook_dict = json.load(file)

for key in notebook_dict:
  print(notebook_dict[key])

with open(NEW_ASSIGNMENT, 'w+', encoding="utf-8") as file:
  json.dump(notebook_dict, file)