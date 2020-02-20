def make_student(ASSIGNMENT):
    ind = ASSIGNMENT.index("INST")
    ext = ASSIGNMENT.index(".ipynb")
    NEW_ASSIGNMENT = ASSIGNMENT[:ind] + "STUDENT" + ASSIGNMENT[ext:]

    with open(ASSIGNMENT, 'r+', encoding="utf-8") as file:
        lines = file.readlines()

    new_lines = []

    LIMIT = len(lines)

    i = 0
    while i < LIMIT:
        # if cell type is code
        if '"code"' in lines[i]:
            found = False
            next_ind = i

            while not found:
                # find the source content of code
                if '"source"' in lines[next_ind]:
                    found = True
                next_ind += 1

            # if the first line of the cell is ANSWER
            if "ANSWER" in lines[next_ind]:
                # delete the first bracket of the cell
                del new_lines[-1]
                # temp variable to hold the lines after the pointer
                temp = lines[i:]
                # find the nearest ending bracket and add one (basically skipping the entire cell)
                i = i + temp.index("  },\n") + 1

            else:
                new_lines.append(lines[i])
                i += 1

        if '"markdown"' in lines[i]:
            found = False
            next_ind = i

            while not found:
                if '"source"' in lines[next_ind]:
                    found = True
                next_ind += 1

            if "ANSWER" in lines[next_ind]:
                del new_lines[-1]
                temp = lines[i:]
                i = i + temp.index("  },\n") + 1
            else:
                new_lines.append(lines[i])
                i += 1
        else:
            new_lines.append(lines[i])
            i += 1

    with open(NEW_ASSIGNMENT, 'w+', encoding="utf-8") as f:
        for l in new_lines:
            f.write(l)

    for line in new_lines:
    	if "ANSWER" in line:
    		print("WARNING! Some answer content may remain in the file. Please double check file contents before administering to students.")
    		break
