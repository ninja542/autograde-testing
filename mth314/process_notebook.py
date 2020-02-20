from traitlets.config import Config
import IPython.core.display as IP
import numpy as np
import sys
import os
import shutil
from instruct.tag_merge import replace_tags
from instruct.strip_output import strip_output
from instruct.make_student import make_student

PROBLEM_FOLDER = sys.argv[1]

# create a custom config object to specify options for nbgrader
config = Config()
# course id
config.CourseDirectory.course_id = "mth314"

try:
    # command = f'rmdir /Q /s "./release/{PROBLEM_FOLDER}"'
    # os.system(command)
    shutil.rmtree(f"./release/{PROBLEM_FOLDER}")
except:
    print("folder doesn't exist")

for filename in os.listdir(f"./source/{PROBLEM_FOLDER}"):
    if filename.endswith(".ipynb"):
        #Calculate Destination name
        ASSIGNMENT = filename
        try:
            ind = ASSIGNMENT.index("INST")
            ext = ASSIGNMENT.index(".ipynb")
            NEW_ASSIGNMENT = ASSIGNMENT[:ind] + "STUDENT" + ASSIGNMENT[ext:]
        except:
            print(f"Skipping file {ASSIGNMENT}")
            continue
        # print("Removing existing student version")

        # remove existing student version
        try:
            # command = f'del "./source/{PROBLEM_FOLDER}/{NEW_ASSIGNMENT}"'
            # os.system(command)
            os.remove(f"./source/{PROBLEM_FOLDER}/{NEW_ASSIGNMENT}")
        except:
            print("No file exists")

        try:
            # command = f"python ./instruct/mailmerge.py ./source/{PROBLEM_FOLDER}/{ASSIGNMENT}"
            # os.system(command)
            replace_tags(f"./source/{PROBLEM_FOLDER}/{ASSIGNMENT}")
        except:
            print("tags failed")

        # strip answer lines and strip notebook output
        try:
            # command = f"python ./instruct/nbstripout.py ./source/{PROBLEM_FOLDER}/{ASSIGNMENT}"
            # os.system(command)
            strip_output(f"./source/{PROBLEM_FOLDER}/{ASSIGNMENT}")
            # command = f"python ./instruct/makeStudentVersion.py ./source/{PROBLEM_FOLDER}/{ASSIGNMENT}"
            # os.system(command)
            make_student(f"./source/{PROBLEM_FOLDER}/{ASSIGNMENT}")

        except:
            print("strip failed")

try:
    command = f"nbgrader generate_assignment {PROBLEM_FOLDER}"
    os.system(command)
except:
    print("Assignment already generated")
