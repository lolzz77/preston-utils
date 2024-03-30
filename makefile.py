import sys
import re
import subprocess
import os
import shutil
import subprocess
import re

if len(sys.argv) < 3:
    print("Invalid number of argument.")
    sys.exit(1)

makefile_path = sys.argv[1]
maekfile_command = sys.argv[2] # the passed in command for this makefile
current_path = os.getcwd()

makefile_python_output_path = current_path + '/makefile_python_output'

if not os.path.exists(makefile_python_output_path):
    os.makedirs(makefile_python_output_path)

makefile_database_path = makefile_python_output_path + '/makefile_database.txt'
makefile_preprocessed_path = makefile_python_output_path + '/makefile_preprocessed.mk'
temp_makefile_path = makefile_python_output_path + '/temp_makefile.mk'

temp_makefile_content = []

# Matches ${...}, $(...)
variable_regex = r'\$[\(\{][a-zA-Z0-9_-]+[\)\}]'

makefile_database_file = open(makefile_database_path, "w")


# Pre-processing, settle all the guardings
with open(makefile_path, "r") as file:
    lines = file.readlines()
    has_guarding = False
    prepare_for_war = False
    temp_temp_makefile_content = []
    # this is for appending to the official write buffer
    temp_temp_temp_makefile_content = []
    separator = 0
    separator_list = []
    # this is for cases like
    # ifeq...
    # else ifeq...
    # endif
    # so, it's a nested ifeq, i have to know which evaluaetes to true
    nest_level = 0
    nest_level_finalized = 0
    guard_nest_level = 0
    for line_4 in lines:
        separator += 1
        temp_line = line_4.lstrip()

        if has_guarding:

            if temp_line.startswith('ifeq') or \
                temp_line.startswith('ifneq'):
                guard_nest_level += 1

                temp_temp_makefile_content.append(line_4)
                nest_level += 1
                temp_temp_makefile_content.append(f"$(info PREPROCESS {nest_level})\n")
                temp_temp_temp_makefile_content.append(line_4)
                separator_list.append(separator)
                continue


            if temp_line.startswith('endif'):
                temp_temp_makefile_content.append(line_4)
                guard_nest_level -= 1
            
            if temp_line.startswith('endif') and\
                guard_nest_level == 0:
                temp_temp_makefile_content.append(line_4)
                temp_temp_temp_makefile_content.append(line_4)
                has_guarding = False
                prepare_for_war = True
                separator_list.append(separator)
            elif temp_line.startswith('else'):
                nest_level += 1
                temp_temp_makefile_content.append(line_4)
                temp_temp_makefile_content.append(f"$(info PREPROCESS {nest_level})\n")
                separator_list.append(separator)
                temp_temp_temp_makefile_content.append(line_4)
                continue
            else:
                temp_temp_temp_makefile_content.append(line_4)
                continue
        
        # write to a preprocessed file
        # then execute `make` on that file
        # get returned output from that file
        # decides which part of code to be included
        if prepare_for_war:
            temp_temp_temp_temp_maekfile_content = []
            temp_temp_temp_temp_maekfile_content = temp_makefile_content.copy()
            temp_temp_temp_temp_maekfile_content.extend(temp_temp_makefile_content)
            temp_temp_makefile_content = []
            with open(makefile_preprocessed_path, "w") as file_3:
                file_3.write(''.join(temp_temp_temp_temp_maekfile_content))
                file_3.flush()
            prepare_for_war = False

            process = subprocess.Popen(['make', '-f', makefile_preprocessed_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=os.environ.copy())
            output, error = process.communicate()

            # strip "PREPROCESSED " (with whitepace) & newline at the end
            output_stripped = output.decode("utf-8")[len("PREPROCESS "):-1]
            nest_level_finalized = int(output_stripped)
            
            # this is a bit complex, so hear me out
            # separator_list will hold index start of `ifeq`, `ifneq`, `else`, `endif`
            # eg:
            # the temp_temp_temp_makefile list = ['ifeq ($(OS_TYPE_VER),LK4)\n', '\tVALUE A\n', 'else\n', '\tVALUE B\n', 'endif\n']
            # separator = [0, 2 ,4]
            # if `else` is evaluated to TRUE,
            # nest_level_finalized = 2
            # if nest_level_finalized = 2, means i need start and end index from index 1 to 2 in the list
            # [0, 2, 4]
            #    1  2
            # what's between 2 is index 1 and index 2
            # index 1 value is 2
            # index 2 value is 4
            # Thus, i need remove index 0 from the list
            # so that i can do separator_list[0] and separator_list[1] to get the start and end value i need
            # then, using star tand end value, which is 2 and 4
            # i can strip the temp_temp_temp_makefile starting from index 2 to index 4
            # End result, i will get temp_temp_temp_makefile list = ['\tVALUE B\n']
            # Update: i changed to instead of popping the list, replace the content of string to newline
            for _ in range(nest_level_finalized-1):
                separator_list.pop(0)

            start = separator_list[0] + 1
            end = separator_list[1]
            separator_list = []
            separator = 0
            nest_level = 0
            nest_level_finalized = 0

            for index_2, line_5 in enumerate(temp_temp_temp_makefile_content):
                if index_2 >= start and index_2 < end:
                    continue
                temp_temp_temp_makefile_content[index_2] = '\n'
            temp_makefile_content.extend(temp_temp_temp_makefile_content)
            temp_temp_temp_makefile_content = []
            continue
        
        if temp_line.startswith('ifeq') or temp_line.startswith('ifneq'):
            has_guarding = True
            temp_temp_makefile_content.append(line_4)
            nest_level += 1
            temp_temp_makefile_content.append(f"$(info PREPROCESS {nest_level})\n")
            temp_temp_temp_makefile_content.append(line_4)
            guard_nest_level += 1
            separator = 0
            separator_list.append(separator)
        else:
            temp_makefile_content.append(line_4)

with open(makefile_preprocessed_path, "w") as file_3:
    file_3.write(''.join(temp_makefile_content))
    file_3.flush()
sys.exit()
# Open the main makefile that you're going to put your build command into
with open(makefile_path, "r") as file:
    lines = file.readlines()
    for index, line in enumerate(lines):
        temp_makefile_content.append(line)

        # search for all variables
        if re.search(variable_regex, line):
            matches = re.findall(variable_regex, line)
            for match in matches:
                # Search weather this variable is existed in the databse
                makefile_database_file.seek(0)

                # Just wanna make it to write `$(info VAR=$(VAR))`
                # So when run make, it will print `VAR=value`
                match_string = match
                match_string = match_string.replace('${', '').replace('}', '')
                match_string = match_string.replace('$(', '').replace(')', '')
                
                string_to_search_for = match_string + '='
                
                # because i changed to open the file always to truncate it
                # then when do readlines() will fail with exception
                # the solution is to close and open with `r` option again, `a` those does not work
                makefile_database_file.close()
                makefile_database_file = open(makefile_database_path, "r")
                
                makefile_database_lines = makefile_database_file.readlines()

                # after reading lines, close the file and reopen again with append mode
                # for writing operation later
                makefile_database_file.close()
                makefile_database_file = open(makefile_database_path, "a")
                
                # Search weather this variable existed in database
                found = False
                the_value = ''
                # reason why i put line_2, cos, it will disturb the original `line` that i had above LOL
                for line_2 in makefile_database_lines:
                    found = False
                    # because i added to print line number, like this `123:abc`
                    # now, i want to strip `123`
                    stripped_line = line_2.split(":")[2]
                    if stripped_line.startswith(string_to_search_for):
                        found = True
                        # get the value
                        # eg: the line is like this
                        # ROOTPATH=/user/home
                        # the valeu will be `/user/home`
                        the_value = line_2[line_2.index(string_to_search_for) + len(string_to_search_for):].strip()
                        break
                
                # Regardless if database contains the variable, evaluates the value
                # Because what if the variable has changed value?
                with open(temp_makefile_path, "w") as file_2:
                    temp_temp_makefile_content = temp_makefile_content.copy()
                    temp_temp_makefile_content.append(f"$(info {match_string}={match})\n")
                    # the content only be written after the file descriptor is closed, well, unless you call file.flush()
                    file_2.write(''.join(temp_temp_makefile_content))

                # Call a process to execute `make` command, copy my current environment to it
                process = subprocess.Popen(['make', '-f', temp_makefile_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=os.environ.copy())
                # Example output
                # Output : b'<the value of {match}\n'
                # error : make: *** no targets. Stop.\n'
                # the `b` infront, is not count in the character, it basically means it is displaying in binrary format i guess
                output, error = process.communicate()
                # this is to remove '\n' at the end
                output_stripped = output.decode("utf-8")[:-1]
                # Then, there are cases where `MAKE=\n ERROR`
                # whereby the error message is printed after the '\n'
                output_stripped = output_stripped.split('\n', 1)[0]
                # remove trailing whitespace, else, later compare `==` will treat it differently
                output_stripped = output_stripped.strip()
                line_number = str(index+1)
                output_to_write.append(makefile_path + ':' + line_number + ':' + output_stripped + '\n')
                # this is for the matching later, i dont want to write into database if
                # PATH=abc already existed in the database
                # But if PATH=def, that is, same varaible name, but different value, then write into database
                output_to_match_for_the_value = output_stripped
                output_to_match_for_the_value = output_to_match_for_the_value[len(string_to_search_for):]

                if found:
                    # If database contains the variable, check whether the value is the same
                    # if diff value, WRITE IT TO DATABASE
                    if the_value != output_to_match_for_the_value and \
                        output:
                        makefile_database_file.write(''.join(output_to_write))
                        makefile_database_file.flush()

                else:
                    # else, write into database
                    # only write when `output` has something
                    if output:
                        makefile_database_file.write(''.join(output_to_write))
                        makefile_database_file.flush()
                    
        # search for included makefile
        if line.startswith('include'):
            # first, we have to find whether there's variable in the path
            # eg: include ../$(WORKSPACE)/path/to/Makefile
            temp_line = line
            makefile_database_file.close()
            makefile_database_file = open(makefile_database_path, "r")
            makefile_database_lines = makefile_database_file.readlines()
            matches = re.findall(variable_regex, line)

            # If there is, replace the variable with the value found in the database
            for match in matches:
                match_string = match
                match_string = match_string.replace('${', '').replace('}', '')
                match_string = match_string.replace('$(', '').replace(')', '')
                string_to_search_for = match_string + '='
            
                for line_3 in makefile_database_lines:
                    stripped_line = line_3.split(":")[2]
                    if stripped_line.startswith(string_to_search_for):
                        the_value = line_3[line_3.index(string_to_search_for) + len(string_to_search_for):].strip()
                        temp_line = line.replace(match, the_value)
                        break

            # no need + '\n', the `line` already included it
            # if you put, above code will error out of index when doing stripping
            output_to_write.append(makefile_path + ':' + str(index + 1) + ':' + temp_line)
            makefile_database_file.close()
            makefile_database_file = open(makefile_database_path, "a")
            makefile_database_file.write(''.join(output_to_write))
            makefile_database_file.flush()

            # line = include ../path/to/directory\n
            # strip `include`, leading whitespace, and the '\n'
            # no need check whether the path contains name.mk or not, it still works for command `make -f /dir/`
            append_path = temp_line.strip('include').strip().rstrip('\n')
            # get the path of the current opened makefile
            # strip `makefile` from the string, append the path of the `line` into it
            current_makefile = makefile_path
            if current_makefile.endswith("Makefile"):
                current_makefile = current_makefile[:-8]

            # sometimes, append_path = ../path/to/Makefile
            # sometimes, append_path = /data/path/to/Makefile
            # if is full path, dont append
            if append_path.startswith('..'):
                new_makefile_path = current_makefile + append_path
            else:
                new_makefile_path = append_path
            process = subprocess.Popen(['make', '-f', new_makefile_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=os.environ.copy())
            output, error = process.communicate()
            print(output)
            print(error)

makefile_database_file.close()
print("Script Ends")