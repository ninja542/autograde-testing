# New Documentation for nbgrader

The original instructor files are made in the *assignment_name* folder inside the _**source**_ folder.

The files inside the source folder are converted into the assignment files and header and footers are added and then placed in the _**release**_ folder.

The students work on their own version of the assignment files, and the files are placed inside the _**submitted**_ folder in the folder structure as shown: **submitted** -> **student name** -> **assignment name** -> **file**. 

# Processing the notebooks

process_notebook.py converts the files in the source folder to the student version by stripping ANSWER cells and stripping output and then using nbgrader to generate the assignments to put the files into the release folder.

The D2L python script from Dr. Colbry will take files from students and place them into the submitted folder. 