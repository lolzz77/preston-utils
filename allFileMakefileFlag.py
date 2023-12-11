# Prerequisite
# pip install pathlib

# Command
# python allFileMakefile.py repo_path/

# Must put '/' at the end, else below code will concatenate repo_pathtrbo
# which makes the path invalid

import glob
import os
import sys
from pathlib import Path
import re

search_text_1 = '-Wall'
search_text_2 = '-Werror'
search_text_3 = '-Wno-uninitialized'
search_text_4 = '-Wno-unused-variable'
search_text_5 = '-Wunused-variable'
search_text_6 = '-Wunused-parameter'
search_text_7 = '-Wno-unused-parameter'
# search_text_8 = '-Wextra'
# search_text_9 = '-Wshadow'
# search_text_10 = '-Wswitch-default'
# search_text_11 = '-Wswitch-enum'
# search_text_12 = '-Wconversion'
# search_text_13 = '-Wno-return-type'
# search_text_14 = '-Wno-unknown-pragmas'
# search_text_15 = '-Wtype-limits'
# search_text_16 = '-Wstrict-prototypes'
# search_text_17 = '-Wno-write-strings'
# search_text_18 = '-Wl'
# search_text_19 = '-Wno-sign-compare'
# search_text_20 = '-Wdeclaration-after-statement'
# search_text_21 = '-fno-strict-aliasing'
# search_text_22 = '-Wno-format'
# search_text_23 = '-Wno-error'
# search_text_24 = '-Wundef'

replace_text = ''
FILE_EXTENSION_MAKEFILE = '*.mk'
GIT_IGNORE_CMD = 'git check-ignore -v'
is_multiline = False

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
repo_path = repo_path + 'trbo'

# using glob to search for .mk file
for path in Path(repo_path).rglob(FILE_EXTENSION_MAKEFILE):
    # Check 'git check-ignore -v'
    # 'cd path; git check-ignore -v filename'
    ret = os.system('cd ' + str(path.parent) + ';' + GIT_IGNORE_CMD + ' ' + str(path.name))
    if(None == ret):
        continue

    print('Opening ' + str(path))

    # Read file, put them in buffer, modify buffer, then rewrite the whole file
    # Opening our text file in read only
    # mode using the open() function
    with open(str(path), 'r') as file:
        # Reading the content of the file
        # using the read() function and storing
        # them in a new variable
        data = file.read()

        # # readlines will read ALL lines
        # old_makefile = file.readlines()

        # # the technique is to store whole content into variable, then modify variable
        # # then write the new variable into the file.
        # # instead of read line by line in the file and modify each line.
        # new_makefile = []
        # for line in old_makefile:
        #     if '-W' in line or is_multiline:
                # print(line)
            #     if '#' in line:
            #         continue
            #     if '\\' in line:
            #         is_multiline = True
            #         if '=' in line:
            #             # u cannot do this, u can, but after that, new_makefile is not 'list' type anymore
            #             # if you happent o call new_makefile.append() after this line, it will be invalid
            #             # new_makefile = re.sub(r'=.+', '=', new_makefile)
            #             line = re.sub(r'=.+', '=', line)
            #             new_makefile.append(line)
            #         continue
            #     line = re.sub(r'=.+', '=', line)
            #     new_makefile.append(line)
            #     is_multiline = False
            # else:
            #     new_makefile.append(line)

        # Searching and replacing the text
        # using the replace() function

        # globals() is used to check if variable is defined, u can safely comment out the variable n wont cause compile error
        if 'search_text_1' in globals() \
            and search_text_1 in data:
            data = data.replace(search_text_1, replace_text)
        if 'search_text_2' in globals() \
            and search_text_2 in data:
            data = data.replace(search_text_2, replace_text)
        if 'search_text_3' in globals() \
            and search_text_3 in data:
            data = data.replace(search_text_3, replace_text)
        if 'search_text_4' in globals() \
            and search_text_4 in data:
            data = data.replace(search_text_4, replace_text)
        if 'search_text_5' in globals() \
            and search_text_5 in data:
            data = data.replace(search_text_5, replace_text)
        if 'search_text_6' in globals() \
            and search_text_6 in data:
            data = data.replace(search_text_6, replace_text)
        if 'search_text_7' in globals() \
            and search_text_7 in data:
            data = data.replace(search_text_7, replace_text)
        if 'search_text_8' in globals() \
            and search_text_8 in data:
            data = data.replace(search_text_8, replace_text)
        if 'search_text_9' in globals() \
            and search_text_9 in data:
            data = data.replace(search_text_9, replace_text)
        if 'search_text_10' in globals() \
            and search_text_10 in data:
            data = data.replace(search_text_10, replace_text)
        if 'search_text_11' in globals() \
            and search_text_11 in data:
            data = data.replace(search_text_11, replace_text)
        if 'search_text_12' in globals() \
            and search_text_12 in data:
            data = data.replace(search_text_12, replace_text)
        if 'search_text_13' in globals() \
            and search_text_13 in data:
            data = data.replace(search_text_13, replace_text)
        if 'search_text_14' in globals() \
            and search_text_14 in data:
            data = data.replace(search_text_14, replace_text)
        if 'search_text_15' in globals() \
            and search_text_15 in data:
            data = data.replace(search_text_15, replace_text)
        if 'search_text_16' in globals() \
            and search_text_16 in data:
            data = data.replace(search_text_16, replace_text)
        if 'search_text_17' in globals() \
            and search_text_17 in data:
            data = data.replace(search_text_17, replace_text)
        if 'search_text_18' in globals() \
            and search_text_18 in data:
            data = data.replace(search_text_18, replace_text)
        if 'search_text_19' in globals() \
            and search_text_19 in data:
            data = data.replace(search_text_19, replace_text)
        if 'search_text_20' in globals() \
            and search_text_20 in data:
            data = data.replace(search_text_20, replace_text)
        if 'search_text_21' in globals() \
            and search_text_21 in data:
            data = data.replace(search_text_21, replace_text)
        if 'search_text_22' in globals() \
            and search_text_22 in data:
            data = data.replace(search_text_22, replace_text)
        if 'search_text_23' in globals() \
            and search_text_23 in data:
            data = data.replace(search_text_23, replace_text)
        if 'search_text_24' in globals() \
            and search_text_24 in data:
            data = data.replace(search_text_24, replace_text)

    # Rewrite the modified buffer into the same file, replacing them all
    # Opening our text file in write only
    # mode to write the replaced content
    with open(str(path), 'w') as file:

        # Writing the replaced data in our
        # text file
        file.write(data)
        # file.writelines(new_makefile)

# End
print("Operation finished.")
