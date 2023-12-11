# Prerequisite
# pip install pathlib

# Command
# python allFileMakefile.py repo_path/

# Must put '/' at the end, else below code will concatenate repo_pathtrbo
# which makes the path invalid

# Global variable used to control you want to put repo_path as argument or custom repo_path/trbo/gemstones/gemstones etc path
IS_REPO_PATH = True
# IS_REPO_PATH = False

import glob
import os
import sys
from pathlib import Path
import re

FILE_EXTENSION_MAKEFILE = '*.mk'
GIT_IGNORE_CMD = 'git check-ignore -v'
is_multiline = False

# input in temrinal:
# python allFileMakefile.py repo
# print(len(sys.argv))
# will output 2
if IS_REPO_PATH:
    if(len(sys.argv) != 2):
        print("No repo passed! Terminating script")
        sys.exit()

print("Begin Operation.")

# input in temrinal:
# python allFileMakefile.py repo
# argv[0] == allFileMakefile.py
# argv[1] == repo
repo_path = sys.argv[1]
if IS_REPO_PATH:
    repo_path = repo_path + 'trbo'

# using glob to search for .mk file
# there are 2: glob and rglob. 'r' stands for recursive. 'glob' only search in current dir
for path in Path(repo_path).rglob(FILE_EXTENSION_MAKEFILE):
    # Check 'git check-ignore -v'
    # 'cd path; git check-ignore -v filename'
    ret = os.system('cd ' + str(path.parent) + ';' + GIT_IGNORE_CMD + ' ' + str(path.name))
    if(None == ret):
        continue

    print('Opening ' + str(path))

    # Read file, put them in buffer, modify buffer, then rewrite the whole file
    with open(str(path), 'r') as file:
        # read data and put each line into array
        lines = file.readlines()
        # Loop thru the array
        for i, line in enumerate(lines):
            # check if 1st index of the line, is alphabet or didgit or '.'
            # If it is, print $(info) on the previous line
            if (line[0].isalpha() or line[0].isdigit() or line[0] == '.'):
                # Check if the current line is 0, cos you can't print on array[-1]
                if i == 0: 
                    j = 0 
                else: 
                    j = 1
                # if prev line, on the 1st index, the char is NOT equal to \n, then no need write, skip
                if lines[i-j][0] != '\n':
                    continue
                # else, write $(info) on the prev line
                # $(MAKECMDGOALS) is global variable that holds target recipe name, eg: make help, will print 'help'
                lines[i-j] = ('$(info MEE ' + str(path) + ' ' + str(i) + '$(MAKECMDGOALS)' + ')\n')

    # Rewrite the modified buffer into the same file, replacing them all
    with open(str(path), 'w') as file:
        # Write the modified buffer into file
        file.writelines(lines)

# End
print("Operation finished.")
