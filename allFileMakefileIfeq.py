# Prerequisite
# pip install pathlib

# Command
# python allFileMakefile.py repo_path/

# Must put '/' at the end, else below code will concatenate repo_pathtrbo
# which makes the path invalid

# Global variable used to control you want to put repo_path as argument or custom repo_path/trbo/gemstones/gemstones etc path
# IS_REPO_PATH = True
IS_REPO_PATH = False

import glob
import os
import sys
from pathlib import Path
import re

GIT_IGNORE_CMD = 'git check-ignore -v'
is_multiline = False

# color
mk_red = 'red:=$(shell tput setaf 1)\n'
mk_green = 'green:=$(shell tput setaf 2)\n'
mk_yellow = 'yellow:=$(shell tput setaf 3)\n'
mk_blue = 'blue:=$(shell tput setaf 4)\n'
mk_reset = 'reset:=$(shell tput sgr0)\n'

# regex

# match target recipe, but not those $(VAR): target recipe
# regex = r'^\S+?:'

# match target recipe except those start with '.' (e.g .PHONY:), and also but not those $(VAR): target recipe
# regex = r'^[^.\s]+?:'

# only matches $(VARIABLE) target recipe
# regex = r'^\s*\$\(([a-zA-Z0-9_-]+)\)\s*:\s*(.*)$'

# matches all target recipe, be it `$(VARIABLE):` or `non-variable:`, and exclude those `VARIABLE := value`, and exclude .PHONY
regex = r'^\s*(?:\$\(([a-zA-Z0-9_-]+)\)|([a-zA-Z0-9_-]+))\s*:(?!=)\s*(.*)$'

# matches all target recipe, be it `$(VARIABLE):` or `non-variable:`, `$(VAR)/%.xxx:`, and exclude those `VARIABLE := value`, and exclude .PHONY
# regex = r'^(?!\.PHONY)\S+:(?!=)'

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

# there are 2: glob and rglob. 'r' stands for recursive. 'glob' only search in current dir
# from the path passed in, get all files, recursively
for path in Path(repo_path).rglob('*'):
    # check if the file is file
    # check if file has extension '.mk'
    # check if file name is named 'makefile'
    # cannot simply just check if file has .mk extension
    # becos all the makefile that name 'makefile' will not have .mk extension
    # if fonud, revserse result
    # Intention: skip non makefile files
    if not (path.is_file() and (path.suffix == '.mk' or path.name.lower() == 'makefile')):
        continue

    # Comming here means makefile is found
    # check if makefile is ignored by git
    # Check 'git check-ignore -v'
    # 'cd path; git check-ignore -v filename'
    ret = os.system('cd ' + str(path.parent) + ';' + GIT_IGNORE_CMD + ' ' + str(path.name))
    if(None == ret):
        continue

    # Coming here means makefile is tracked by git
    print('Opening ' + str(path))

    # Read file, put them in buffer, modify buffer, then rewrite the whole file
    with open(str(path), 'r') as file:
        line_to_write = [] # empty list
        next_line = [] # empty array
        tab = "" # empty string

        # append the color in every makefile
        line_to_write.append(mk_red)
        line_to_write.append(mk_green)
        line_to_write.append(mk_yellow)
        line_to_write.append(mk_blue)
        line_to_write.append(mk_reset)
        # For every makefile, append a log at the beginning
        line_to_write.append('$(info $(yellow)MEE ' + str(path) + ' TRIGGERED$(reset))\n')
        
        # read data and put each line into array
        lines = file.readlines()

        # Loop thru the array
        for i, line in enumerate(lines):
            # put each line into new variable, then append n modify this 'line_to_write' variable
            # intention: i want to append new line, but i cannot modify the original 'lines' variable
            # it will mess up the line reading later
            line_to_write.append(line)

            # Check if 'i' is at maximum
            if i == (len(lines) - 1):
                next_line = None
            else:
                next_line = lines[i+1]

            # comment, skip
            if line.startswith('#'):
                continue

            # This 'if' will handle whether the log should print '\t' or not
            # If print log inside target recipe, you have to put '\t'
            # If is non target recipe, then no need put '\t', else you get 'recipe commences before first target.  Stop.'
            if re.match(regex, line):
                # is target recipe, have to put tab
                tab = '\t'
                # calculate the line num
                line_num = len(line_to_write) + 1
                # write log for target recipe
                line_to_write.append(tab + '$(info $(green)MEE ' + str(path) + ' ' + str(line_num) + ' TARGET RECIPE' + '$(reset))\n')

            # FYI
            # any ifeq ifneq that is within target recipe, they do not require putting '\t'
            #
            # Example:
            # all:
            #   $(CC)...
            # ifeq()        # here, ifeq() do not need '\t'
            #   $(CC)...
            #
            # thus, if detected next line is without '\t', but it starts with ifeq ifneq etc, it is still within target recipe

            # if not match the following, means it is not part of target recipe
            # and no '\t' is required
            #
            # Reason to put 'endif', for this case
            # in this case, search '-@echo -z -q -a -c -m"$(FZAP_MAP)" -o"$@" -w -x > $(L3LKF)' if part of target recipe '$(FZAP_OUT): in following code
            # after 'endif', the subsequence code is still part of target recipe
            #
            # ifeq ($(FREON), secure)
            # $(FZAP_OUT): $(DATALIGHT_FFX_LIB) $(EMMC_LIB) $(OBJECT_FILES) $(LINK_CMD_FILE)
            # else
            # $(FZAP_OUT): $(DATALIGHT_FFX_LIB) $(EMMC_LIB) $(OBJECT_FILES) $(LINK_CMD_FILE) $(MBED_TLS_LIBS) $(SW_VERIFICATION_OBJ)
            # endif
            # 
            # ifeq ($(FREON), secure)
            # 	-@echo -z -q -a -c -m"$(FZAP_MAP)" -o"$@" -w -x > $(L3LKF)
            # else
            # 	-@echo --abi=ti_arm9_abi -z -q -a -c -m"$(FZAP_MAP)" -o"$@" -w -x > $(L3LKF)
            # endif
            # 	-@echo $(foreach obj, $(OBJECT_FILES), "$(obj)") >> $(L3LKF)
            # 	-@echo $(LNKOPS) >> $(L3LKF)
            # 	-@echo "$(LINK_CMD_FILE)" >> $(L3LKF)
            # 	$(CC) -@"$(L3LKF)"
            #
            if  not line.startswith(('ifeq', 'ifneq', 'else', 'endif', '\t', '\n')) and \
                not re.match(regex, line):
                tab = ''

            # The following puts log for 'ifeq' and etc cases
            # tokenize the strings from the line
            tokens = line.split()
            # loop thru each token
            for token in tokens:
                if token in ('ifeq', 'ifneq', 'else'):
                    # get total lines of array
                    line_num = len(line_to_write) + 1
                    # write log
                    # $(MAKECMDGOALS) is global variable that holds target recipe name, eg: make help, will print 'help'
                    line_to_write.append(tab + '$(info $(green)MEE ' + str(path) + ' ' + str(line_num) + ' $(MAKECMDGOALS)' + '$(reset))\n')
                # once written 1 time, break, there are cases 'else ifneq' tgt, causing it to writen log 2 times
                break

    # Rewrite the modified buffer into the same file, replacing them all
    with open(str(path), 'w') as file:
        # Write the modified buffer into file
        file.writelines(line_to_write)

# End
print("Operation finished.")
