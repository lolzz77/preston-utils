# Prerequisite
# pip install pathlib

# Command
# python allFileMakefile.py file_path

# This script will append "MEE ${line number}" log in every line, for bash script file

import os
import sys
from pathlib import Path
import re

# input in temrinal:
# python allFileMakefile.py repo
# print(len(sys.argv))
# will output 2
if(len(sys.argv) != 2):
    print("No repo passed! Terminating script")
    sys.exit()

print("Begin Operation.")

# input in temrinal:
# python allFileMakefile.py repo
# argv[0] == allFileMakefile.py
# argv[1] == repo
repo_path = sys.argv[1]

print('Opening ' + str(repo_path))

# global variable
# this is for tallying each line number
# this is to handle if new line '${variable}' is added, thus, increase line num by 1
g_additional_line = 0

# Read file, put them in buffer, modify buffer, then rewrite the whole file
with open(str(repo_path), 'r') as file:
    # Grab all '${variable name}'
    # I want to print out its value
    pattern = r'\${(.*?)}'

    insert_line = ''
    line_num = 0
    skip = False
    matches = []
    offset_line_num = 0

    # read data and put each line into array
    lines = file.readlines()
    # Loop thru the array
    for i, line in enumerate(lines):

        # To handle case like 
        # ------------------
        # var = "hello \
        # world"
        # ------------------
        # then, do not add my lines after '\' line
        # Technique: check on previous line
        # So, if i == 0, there's no previous line
        # get previous line
        check_line = lines[i-1]
        # rstrip() is to remove trailing characters like whitespace etc
        check_line = check_line.rstrip()
        if check_line.endswith('\\'):
            # check if got '${variable name}' on CURRENT line, because we're about to skip this loop
            matches = matches + re.findall(pattern, line)
            # have to decrement by 1, else later line number will not tally
            g_additional_line -= 1
            continue

        # trying to print line number here
        # because im adding 'echo' on every line with '\n' at the end
        # i found that, every line added will cos the line number doubled
        line_num = i #Get original line num
        line_num *= 2 #double it
        line_num += 1 #plus 1, cos index starts at 0, line starts at 1
        line_num += g_additional_line #in case got add '${variable name}' line, then need add this global variable so the line number tally

        insert_line = 'echo "MEE ' + str(line_num) + '"' + '\n'

        # Grab all '${variable name}'
        # 'findall' returns a list
        # concatenate list instead of appending a list into another list
        matches = matches + re.findall(pattern, line)
        # j - the index num for each loop, use to add into line number. Does not mean get the index of the 'matches' list
        # enumarate(matches, 1) - means start index num at 1
        for j, word in enumerate(matches, 1):
            # since 'matches' got match, then increase num by 1
            g_additional_line += 1
            insert_line = insert_line + 'echo "MEE ' + str(line_num + j) + ' ' + word + ' = "' + '${' + word + '}' + '\n'

        # concatenate my lines with original line
        lines[i] = insert_line + line

        # Reset
        matches = []
        insert_line = ''
        

# Rewrite the modified buffer into the same file, replacing them all
with open(str(repo_path), 'w') as file:
    # Write the modified buffer into file
    file.writelines(lines)

# End
print("Operation finished.")
