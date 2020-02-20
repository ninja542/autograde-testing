import sys
from IPython.core.display import Javascript, HTML
from IPython.display import display
import csv
import datetime
import calendar

# ASSIGNMENT = sys.argv[1]
# NEW_ASSIGNMENT = ASSIGNMENT[:ind] + "STUDENT" + ASSIGNMENT[ext:]
# ind = ASSIGNMENT.index("INST")
# ext = ASSIGNMENT.index(".ipynb")

tags = {}

def replace_tags(ASSIGNMENT):
    assignment_str = ASSIGNMENT.split("/")[-1]

    with open(ASSIGNMENT, 'r+', encoding="utf-8") as file:
        lines = file.readlines()
    print("Finding and replacing tags")
    try:
        month=int(assignment_str[0:2])
        day=int(assignment_str[2:4])

        my_date = datetime.datetime(2020, month, day)
        #my_date = date.today()
        weekday=calendar.day_name[my_date.weekday()]
        mnth=calendar.month_name[month]

        tags['DUE_DATE']=f'{weekday} {mnth} {day}'
        tags['MMDD']=assignment_str[0:4]
    except:
        print("Date not found")

    new_lines=[]
    for row in lines:
        for key in tags:
            if (key in row):
                row = row.replace(f"###{key}###",tags[key])
                print(row)
        new_lines.append(row)

    with open(ASSIGNMENT, 'w+', encoding="utf-8") as f:
        for l in new_lines:
            f.write(l)