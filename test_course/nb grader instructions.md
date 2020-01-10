How to set up nbgrader

---

# INSTALL NBGRADER

`pip install nbgrader`

If you have Anaconda:

`conda install jupyter`
`conda install -c conda-forge nbgrader`

# ACTIVATE NBGRADER

`jupyter nbextension install --sys-prefix --py nbgrader --overwrite`
`jupyter nbextension enable --sys-prefix --py nbgrader`
`jupyter serverextension enable --sys-prefix --py nbgrader`

---

# CREATE NBGRADER COURSE

Navigate to the folder you want to create the course folder in terminal

`nbgrader quickstart course_id`

course_id is the name of the course you want to create

and then start jupyter notebook

---

# OVERVIEW ON FOLDERS IN NBGRADER

```
course_name
	| autograded
	| feedback
	| release
	| source
	| submitted
```

Autograded: Where student notebooks go after being autograded

Feedback: Where generated feedback goes

Release: Where generated assignments go

Source: Where Instructors make the assignment files

Submitted: Where to put student notebooks in

---

# JUPYTER NOTEBOOK

When jupyter notebook is started, click the Formgrader button on the homepage

There is an example problem set that will appear, named "ps1"

There is a button to add new assignments on the page.

When you click on your new assignment, you will be taken to jupyter notebook navigation. Make a new notebook as usual.

In the new notebook, go to View > Cell Toolbar > Create Assignment

There will be a toolbar on top that will let you change what type of cell each cell is.

For regular cells you don't need to touch it.

---

# Types of cells

## MANUALLY GRADED ANSWERS

Mark the cell as Manually Graded Answer, then indicate how many points the problem is worth.

The entire cell will be replaced with a code or text stub

## MANUALLY GRADED TASKS

Mark the cell as Manually Graded Task. Then indicate how many points the problem is worth.

A mark scheme can be created through the use of a special syntax such as `=== BEGIN MARK SCHEME ===` and `=== END MARK SCHEME ===`. The section of text between the two markers will be removed from the student version, but will be visible at the grading stage and in the feedback.

The cell is read-only, so make it clear that students need to put their answers in a different cells. 

## DIFFERENCE BETWEEN ANSWER AND TASKS

The difference with a manually graded answer is that the manually graded tasks cells are not edited by the student. A manually or automatically graded cell ask students to perform a task in one cell. A manually graded task asks students to perform a task with cells.

The common use case for this type of cell is for tasks that require the student to create several cells such as “Process the data and create a plot to illustrate your results.” or to contain notebook-wide tasks such as “adhere to the PEP8 style convention.”

## AUTOGRADED ANSWER CELLS

To mark that a cell contains code that would need to be autograded, mark the cell as Autograded Answer.

Then write the correct solution code

For code you would like to hide, use `### BEGIN SOLUTION` and `### END SOLUTION`

If the markers are not used, then the stuff inside the function will automatically be replaced with the code stub

## AUTOGRADER TEST CELLS

```python 
from nose.tools import assert_equal
assert_equal(function_to_test(input), correct_answer)
```

```python
from nose.tools import assert_raises
assert_raises(someError, function, input)
```

Indicate how many points the autograder tests are worth.

You may hide tests using `### BEGIN HIDDEN TESTS` and `### END HIDDEN TESTS`

Autograder test cells are marked read only by default, they will be replaced with the master version if the student has modified the test cells.

---

# VALIDATE NOTEBOOK

Press the validate button next to the Markdown/Code cell type thing on the top to make sure that your instructor version is correct and the tests are correct.

You can also use the command line

`nbgrader validate source/ps1/*.ipynb`

# GENERATING ASSIGNMENT

Navigate back to Formgrader. There will be a button to generate the assignment (In the generate column). Press it to generate the assignment.

You can also use the command line

`nbgrader generate_assignment "ps1" --IncludeHeaderFooter.header=source/header.ipynb --force`

"ps1" being the assignment name, and you can include a header notebook

# AUTOGRADING ASSIGNMENTS

Put the student assignments into the folder named after the assignment in the student's individual folder in the Submitted Folder

`course_id\submitted\student_id\assignment_name`

Formgrader has a button for individually autograding assignments

but we're here for speed

`nbgrader autograde "ps1" --force`

# MANUALLY GRADING ASSIGNMENTS

Go to Formgrader. Click on Manually Grade Assignments, and go into the assignment. Then click on the name of the first submission. Then start manually grading the manual graded sections. There will be a box after every cell for comments that you can put comments in that show up in the generated feedback html files.

# GENERATE FEEDBACK

Formgrader has a button for individually generating feedback

Command line version:

`nbgrader generate_feedback "ps1"`

# DATABASE EXPORT

To export database to csv file do

`nbgrader export`

and the file `grades.csv` will be created

---

# FOLDER STRUCTURE INFO THAT I COPIED AND PASTED

Here is how a sample directory structure for the course named course101 might look, where the users bitdiddle and hacker have submitted solutions to the assignment ps1:

```
course101/
┝━━ gradebook.db
┝━━ nbgrader_config.py
┝━━ source
│   ┝━━ header.ipynb
│   ┕━━ ps1
│       ┝━━ jupyter.png
│       ┝━━ problem1.ipynb
│       ┕━━ problem2.ipynb
┝━━ release
│   ┕━━ ps1
│       ┝━━ jupyter.png
│       ┝━━ problem1.ipynb
│       ┕━━ problem2.ipynb
┝━━ submitted
│   ┝━━ bitdiddle
│   │   ┕━━ ps1
│   │       ┝━━ jupyter.png
│   │       ┝━━ problem1.ipynb
│   │       ┝━━ problem2.ipynb
│   │       ┕━━ timestamp.txt
│   ┕━━ hacker
│       ┕━━ ps1
│           ┝━━ jupyter.png
│           ┝━━ problem1.ipynb
│           ┝━━ problem2.ipynb
│           ┕━━ timestamp.txt
┝━━ autograded/
┕━━ feedback/
```

Solution delimiters have to be different for nbgrader generator to work, can not use ###ANSWER as both beginning and ending delimiters

It replaces everything inside the code block with the stock text, so comments inside the function are deleted. It's not completely disasterous, but you will have to add comments outside of the answer block. 

Probably could figure out how to process the ipynb notebook first to replace the ### ANSWER stuff wtih the correct delimiters? Plus you have to go through the notebook to add the autograde tests and function to autograde with points.

---

# JSON Metadata

[Link to the Documentation](https://nbgrader.readthedocs.io/en/stable/contributor_guide/metadata.html)

## JSON Analysis for notebooks in the SOURCE folder

### JSON for Autograder tests
```javascript
{
    "metadata": {
        "nbgrader": {
            "grade": true,
            "grade_id": "squares_invalid_input",
            "locked": false,
            "points": 1,
            "schema_version": 3,
            "solution": false
        }
    }
}
```

grade means that this cell is going to get graded, and since there's points and it's a code cell, it will get autograded

points is how many points the cell is

### JSON for Autograded Answer
```javascript
{
    "metadata": {
        "nbgrader": {
            "grade": false,
            "grade_id": "squares",
            "locked": false,
            "schema_version": 3,
            "solution": true
        }
   }
}
```

This indicates that this is a solution cell for students 

### JSON for Manually Graded Answer
```javascript
{
    "metadata": {
        "nbgrader": {
            "grade": true,
            "grade_id": "sum_of_squares_equation",
            "locked": false,
            "points": 1,
            "schema_version": 3,
            "solution": true
        }
    }
}
```

This is a Manually Graded Answer because grade is true, and solution is true which means the cell gets erased, and you have to manually grade the solution.

### JSON for Manually Graded Task

```javascript
{
    "metadata": {
        "nbgrader": {
            "grade": false,
            "grade_id": "cell-938593c4a215c6cc",
            "locked": true,
            "points": 4,
            "schema_version": 3,
            "solution": false,
            "task": true
        }
    }
}
```

This is a Manually Graded Task because grade and solution is false, but the task value is true.

So in the source files, `"solution": true` means that nbgrader has to process the cell first to remove the answer from inside the cell.  

`"grade": true` means that there is grading going on in the cell. Nbgrader decides whether to autograde the cell or not based on the value of `"solution"`

`"locked": true` means that the cell is read-only and will get rewritten when submissions are autograded.

The other markers don't really matter. 

## JSON Analysis for notebooks in the RELEASE folder

The JSON for notebooks in the release folder is practically the same as the notebooks in the SOURCE folder, except there is a `checksum` and `cell_type` in the nbgrader object. 

There is `deleteable` and `editable` in the overall metadata. 


### JSON for Autograded Answer

```javascript
{
    "metadata": {
        "deletable": false,
        "nbgrader": {
            "cell_type": "code",
            "checksum": "8f1eab8d02a9520920aa06f8a86a2492",
            "grade": false,
            "grade_id": "squares",
            "locked": false,
            "schema_version": 3,
            "solution": true
        }
    }
}
```

### JSON for Autograder Tests

```javascript
{
    "metadata": {
        "deletable": false,
        "editable": false,
        "nbgrader": {
            "cell_type": "code",
            "checksum": "8f41dd0f9c8fd2da8e8708d73e506b3a",
            "grade": true,
            "grade_id": "correct_squares",
            "locked": false,
            "points": 1,
            "schema_version": 3,
            "solution": false
        }
    }
}
```

### JSON for Manually Graded Answer

```javascript
{
    "metadata": {
        "deletable": false,
        "nbgrader": {
            "cell_type": "markdown",
            "checksum": "f3cc38a3e522c0be10852ebbe2a638b7",
            "grade": true,
            "grade_id": "sum_of_squares_equation",
            "locked": false,
            "points": 1,
            "schema_version": 3,
            "solution": true
        }
    }
}
```

### JSON for Manually Graded Task

```javascript
{
    "metadata": {
        "deletable": false,
        "editable": false,
        "nbgrader": {
            "cell_type": "markdown",
            "checksum": "987adcce9e8e5119f9c00f2db459fd97",
            "grade": false,
            "grade_id": "cell-938593c4a215c6cc",
            "locked": true,
            "points": 4,
            "schema_version": 3,
            "solution": false,
            "task": true
        }
    }
}
```

