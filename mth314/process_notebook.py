from nbgrader.apps import NbGraderAPI
from traitlets.config import Config
import IPython.core.display as IP
import numpy as np
import sys
import os

PROBLEM_FOLDER = sys.argv[1]

# create a custom config object to specify options for nbgrader
config = Config()
# course id
config.CourseDirectory.course_id = "mth314"

try:
    command = f'rmdir /Q /s "./release/{PROBLEM_FOLDER}"'
    os.system(command)
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
            command = f'del "./source/{PROBLEM_FOLDER}/{NEW_ASSIGNMENT}"'
            os.system(command)
        except:
            print("No file exists")

        # strip answer lines and strip notebook output
        try:
            command = f"python ./instruct/makeStudentVersion.py ./source/{PROBLEM_FOLDER}/{ASSIGNMENT}"
            os.system(command)
            command = f"python ./instruct/nbstripout.py ./source/{PROBLEM_FOLDER}/{ASSIGNMENT}"
            os.system(command)
        except:
            print("strip failed")
        #try:
        #    command = f"rename ./source/{PROBLEM_FOLDER}/{ASSIGNMENT} ./source/{PROBLEM_FOLDER}/{ASSIGNMENT[:-6]}.json"
        #    os.system(command)
        #except:
        #    print("failed rename")
        # replace tags
        try:
            command = f"python ./instruct/mailmerge.py ./source/{PROBLEM_FOLDER}/{ASSIGNMENT}"
            os.system(command)
        except:
            print("tags failed")

try:
    command = f"nbgrader generate_assignment {PROBLEM_FOLDER}"
    os.system(command)
except:
    print("Assignment already generated")



# def merge(this_notebook, studentfolder='./', tags={}):
#     #Move to the working directory
#     print("Moving to working directory")
#     command = f"mv {NEW_ASSIGNMENT} {studentfolder}"
#     os.system(command)