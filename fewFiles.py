# Prerequisite
# pip install pathlib

# Command
# python allFileMakefile.py repo_path/

import include
import glob
import os
import sys
from pathlib import Path
import re

replace_text = ''
is_multiline = False

# input in temrinal:
# run command:
# 'python allFileMakefile.py repo'
# then when u put this code 'print(len(sys.argv))'
# will output 2
if(len(sys.argv) < 2):
    print("No repo passed! Terminating script")
    sys.exit()

print("Begin Operation.")

# input in temrinal:
# python allFileMakefile.py repo
# argv[0] == allFileMakefile.py
# argv[1] == repo

# sys.argv is already a list
# so u no need to tokenize user input
dir_list = sys.argv

# 1st element is always the file name, remove it
dir_list.pop(0)

# Compile a list of regex
regex_list_skip = [
    re.compile(include.POSIX_regex_skip[0]),
    re.compile(include.POSIX_regex_skip[1]),
    re.compile(include.POSIX_regex_skip[2]),
    re.compile(include.POSIX_regex_skip[3]),
    re.compile(include.POSIX_regex_skip[4]),
    re.compile(include.POSIX_regex_skip[5]),
    re.compile(include.POSIX_regex_skip[6]),
    re.compile(include.POSIX_regex_skip[7]),
    re.compile(include.POSIX_regex_skip[8]),
    re.compile(include.POSIX_regex_skip[9]),
    re.compile(include.POSIX_regex_skip[10]),
    re.compile(include.POSIX_regex_skip[11]),
    re.compile(include.POSIX_regex_skip[12]),
    re.compile(include.POSIX_regex_skip[13]),
    re.compile(include.POSIX_regex_skip[14]),
    re.compile(include.POSIX_regex_skip[15])
]
regex_list_match = [
    re.compile(include.POSIX_regex_match[0]),
    re.compile(include.POSIX_regex_match[1]),
    re.compile(include.POSIX_regex_match[2]),
    re.compile(include.POSIX_regex_match[3])
]

for dir_path in dir_list:

    # for path provided in Path() and that matches the glob() recursively, open the file
    # Python will straight away get a list of matched FILE_EXTENSION from the path you provided, and is recursively
    # All those matched files, will be stored in this 'path' variable, and loop them
    for path in Path(dir_path).rglob(FILE_EXTENSION):
        # 'cd path; git check-ignore -v filename'
        ret = os.system('cd ' + str(path.parent) + ';' + GIT_IGNORE_CMD + ' ' + str(path.name))
        if(0 == ret):
            continue

        print('Opening ' + str(path))

        # Opening our text file in read only
        # mode using the open() function
        with open(str(path), 'r') as file:
            # Reading the content of the file
            # using the read() function and storing
            # them in a new variable
            data = file.readlines()

        # Opening our text file in write only
        # mode to write the replaced content
        with open(str(path), 'w') as f:

            # Writing the replaced data in our
            # text file
            file.write(data)
            # file.writelines(new_makefile)

# Printing Text replaced
print("Operation finished.")
