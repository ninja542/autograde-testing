import json
import sys

ASSIGNMENT = sys.argv[1]
ind = ASSIGNMENT.index("INST")
ext = ASSIGNMENT.index(".ipynb")
NEW_ASSIGNMENT = ASSIGNMENT[:ind] + "STUDENT" + ASSIGNMENT[ext:]

with open(ASSIGNMENT, 'r+', encoding="utf-8") as file:
	notebook_dict = json.load(file)

beg_delim = "BEGIN MARK SCHEME"
end_delim = "END MARK SCHEME"

for key in notebook_dict["cells"]:
  try:
    if key["metadata"]["nbgrader"]["grade"] == True and key["metadata"]["nbgrader"]["solution"] == True:
      print("markscheme cell", key["metadata"])
      print(key["source"])
      print(list(filter(lambda x: beg_delim in x, key["source"])))
  except:
    # print("failed")
      pass

  # print(key["metadata"])

# with open(NEW_ASSIGNMENT, 'w+', encoding="utf-8") as file:
  # json.dump(notebook_dict, file)