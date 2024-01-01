# Prerequisite
# pip install pathlib

# Command
# To put log in every entry of functino
# python allFiles.py [repo_path/]
# 
# To put log for caller function
# python allFiles.py [repo_path/] caller [keyword]

import include
import glob
import os
import sys
from pathlib import Path
import re
import subprocess


TEXTMATE_FILE_PATH = './textmate.js'
TEXTMATE_CALLER_FILE_PATH = './textmateCaller.js'
LIBRARY_TO_INCLUDE= '#include <stdio.h>\n'
LOG_TO_WRITE = "\n\tprintf(\"MEE %s:%s:%d\\r\\n\", __FILE__, __FUNCTION__, __LINE__);\n"

replace_text = ''
is_multiline = False

# input in temrinal:
# run command:
# 'python allFileMakefile.py repo'
# then when u put this code 'print(len(sys.argv))'
# will output 2
if(len(sys.argv) < 2):
    print("Wrong argument. Terminating script.")
    sys.exit()

print("Begin Operation.")

# input in temrinal:
# python allFileMakefile.py repo
# argv[0] == allFileMakefile.py
# argv[1] == repo

# sys.argv is already a list
# so u no need to tokenize user input
dir_list = []
dir_list.append(sys.argv[1])

option = ''
if len(sys.argv) > 3:
    option = sys.argv[2]
    caller_keyword = sys.argv[3]

for dir_path in dir_list:


    for file_extension in include.FILE_EXTENSION_C:

        # for path provided in Path() and that matches the glob() recursively, open the file
        # Python will straight away get a list of matched FILE_EXTENSION from the path you provided, and is recursively
        # All those matched files, will be stored in this 'path' variable, and loop them
        for path in Path(dir_path).rglob('*'+file_extension):


            # lousy way to exclude from certain directory
            if 'testsuite' in str(path.parent):
                continue
            if 'test' in str(path.parent):
                continue


            outputs = ''

            # 'cd path; git check-ignore -v filename'
            # Output: .gitignore:46:node_modules      benchmark-native.c
            # os.system will return '0' value
            # This means this path will be ignored by git
            # Else, os.system will return '256' value
            ret = os.system('cd ' + str(path.parent) + ';' + include.GIT_IGNORE_CMD + ' ' + str(path.name))
            if(0 == ret):
                continue

            print('Opening ' + str(path))

            # get file size, if 0, skip, this is for performance
            file_size = os.path.getsize(str(path))
            if file_size == 0:
                continue

            # 0 = success
            # else, probably error
            # ret = os.system('node ' + TEXTMATE_FILE_PATH + ' ' + str(path))
            if option:
                command = 'node ' + TEXTMATE_CALLER_FILE_PATH + ' ' + str(path) + ' ' + str(caller_keyword)
            else:
                command = 'node ' + TEXTMATE_FILE_PATH + ' ' + str(path)

            try:
                outputs = subprocess.check_output(command, shell=True, universal_newlines=True)
                if outputs:
                    # print(outputs)
                    # sys.exit()

                    # expected format : ['60:0', '95:0', '167:0', '']
                    # (line number : index number) that has function opening curly bracket `{`
                    outputs = outputs.split('\n')
            except UnicodeDecodeError:
                print("UnicodeDecodeError: " + str(path))
                continue

            # only read & write when got output
            if not outputs:
                continue

            # Opening our text file in read only
            # mode using the open() function
            # some file will fail to open due to encoding
            try:
                with open(str(path), 'r') as file:
                    # Reading the content of the file
                    # using the read() function and storing
                    # them in a new variable
                    data = file.readlines()

                    # Insert library into 1st line
                    # The way I insert is not append a new line
                    # But rather, get the 1st line, append the string in front of it
                    data[0] = LIBRARY_TO_INCLUDE + data[0]
                    for output in outputs:
                        split = output.split(':')
                        if split[0] == '':
                            continue
                        # python indexing starts at 0
                        # VSCode line number on screen starts at 1
                        # In textmate.js, i put it output to have (i+1)
                        # So that i can easily refer back to which VSCode line is it
                        # However, at there, you gotta make it back to minus 1
                        corrected_line_inedx = int(split[0]) - 1
                        # This string index holds the index of '{'
                        # I want to insert string after this '{'
                        string_index = int(split[1]) + 1
                        # Insert my LOG in between of the string
                        data[corrected_line_inedx] = data[corrected_line_inedx][:string_index] + LOG_TO_WRITE + data[corrected_line_inedx][string_index:]
            except UnicodeDecodeError:
                print("UnicodeDecodeError: " + str(path))
                continue

            # Opening our text file in write only
            # mode to write the replaced content
            with open(str(path), 'w') as file:
                # Writing the replaced data in our
                # text file
                # file.write(data)
                file.writelines(data)

# Printing Text replaced
print("Operation finished.")
