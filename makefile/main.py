# TODO: Implement watchdog, in case unlimited loops, watchdog terinate the script

# Usage : python3 [path to this script] [path to the Makefile you want] ["the command you pass into the Makefile, with double quote"]

# Cautions:
# Prefer not to pass in `-j=` argument (Means run multiple processes at once)
# Cos I didnt test what will be end up lol

# Note:
# you put your preprocessed makefile into /dir/Makefile_Preprocessed.mk
# In that makefile, it has a line `include ../Makefile_2`
# It is using relative path `../`
# Even tho you put in `/dir`
# This `../` will take place at your current directory your terminal is running
# That is, putting your Makefile_Preprocessed.mk in any dir, it wont affact the outcome.
# As long as your terminal is at the right directory, you're fine

# Note:
# By doing subprocess.Popen('bash', '-c', 'path/to/bash/script')
# doesnt solve the debugging to setup the environments
# But in real execution ok
# when you launch debugger, it openup a new terminal
# So i need to make that terminal to setup environment
# But keeps failing
# copying envirnoment no use, cos this code happens only after debugger opened up a new terminal
# so what you copied, is the terminal opened up by debugger
# using task.json also no use

import sys
import re
import subprocess
import os
import shutil
import test

if len(sys.argv) < 2:
    print("Invalid number of argument.")
    sys.exit(1)

makefile_path = sys.argv[1]  # the makefile path

passed_in_command = ''

if len(sys.argv) >= 3:
    # the passed in command for this makefile
    passed_in_command = sys.argv[2]

makefile_command = passed_in_command.split()
makefile_command = [word.strip() for word in makefile_command]

current_path = os.getcwd()
makefile_python_output_path = current_path + '/preston_utils_makefile_output'

# Create my output folder if not exists
if not os.path.exists(makefile_python_output_path):
    os.makedirs(makefile_python_output_path)

# Database, contains all variables and their values
makefile_database_path = makefile_python_output_path + '/makefile_database.txt'
# Preprocessed makefile, remvoe all `ifeq` guarding
makefile_preprocessed_path = makefile_python_output_path + '/makefile_preprocessed.mk'
# Preprocessed makefile with include makefile cpied into it. `include` keyword means copy the content of the makefile and paste into the makefile
makefile_with_include_path = makefile_python_output_path + '/makefile_preprocessed_with_include.mk'
# This is temporary makefile used for `makefile_database_path` to print out the value
temp_makefile_path = makefile_python_output_path + '/temp_makefile.mk'

# always create & truncate the file
makefile_database_file = open(makefile_database_path, "w", encoding='utf-8')
makefile_database_file.close()

make_file_content = []













def preprocess(makefile_path, makefile_preprocessed_path):
    # Pre-processing, settle all the guardings
    with open(makefile_path, "r", encoding='utf-8') as file:
        has_guarding = False
        prepare_for_war = False
        is_target_recipe = False
        lines_2 = []
        temp_makefile_content = []
        temp_temp_makefile_content = []
        temp_temp_temp_makefile_content = []
        # this is for appending to the official write buffer
        temp_temp_temp_temp_makefile_content = []
        # this is for cases like
        # ifeq...
        # else ifeq...
        # endif
        # so, it's a nested ifeq, i have to know which evaluaetes to true
        guard_nest_level = 0
        temp_line = ''
        temp_temp_line = ''
        temp_temp_temp_line = ''
        temp_temp_temp_temp_line = ''
        temp_temp_temp_temp_temp_line = ''
        temp_temp_temp_temp_temp_temp_line = ''
        command = []
        process = None
        output = None
        error = None
        error_decoded = ''
        error_list = []
        output_decoded = ''
        output_list = []
        index_3 = 0
        output_list_0 = ''
        match_2 = None
        is_backward_slash = False

        lines_2 = file.readlines()
        for index_8, line_4 in enumerate(lines_2):
            temp_line = line_4.lstrip()  # trim leading whitespace
            temp_temp_temp_line = line_4[:-1]  # remgit stove newline at the end
            # Given $(ABC)=1,
            # Replace $(ABC) to $$(ABC), so that when you run the makefile code,
            # It will output `$(ABC)` instead of `1`
            temp_temp_temp_line = temp_temp_temp_line.replace("$(", "$$(")
            temp_temp_temp_line = temp_temp_temp_line.replace("${", "$${")
            # Reason i put `""`,
            # Given `     $(ABC)`
            # When you run makefile code,
            # It will output the whitespace as well
            # But in the output, it will output `""`, so you gotta remove it later
            temp_temp_line = f'$(info "{index_8+1}:{temp_temp_temp_line}")\n'

            if line_4.isspace(): # if the line is just whitespace & newline, just make it into newline
                temp_temp_line = '\n'

            if has_guarding:

                if temp_line.startswith('ifeq') or \
                    temp_line.startswith('ifneq'):
                    guard_nest_level += 1

                    temp_temp_makefile_content.append(line_4)
                    temp_temp_temp_makefile_content.append(line_4)
                    continue

                if temp_line.startswith('endif'):
                    temp_temp_makefile_content.append(line_4)
                    guard_nest_level -= 1
                
                if temp_line.startswith('endif') and\
                    guard_nest_level == 0:
                    temp_temp_temp_makefile_content.append(line_4)
                    has_guarding = False
                    prepare_for_war = True
                elif temp_line.startswith('else'):
                    temp_temp_makefile_content.append(line_4)
                    temp_temp_temp_makefile_content.append(line_4)
                    continue
                else:
                    # if is `endif` line, dont append
                    if temp_line.startswith("endif"):
                        pass
                    else:
                        temp_temp_makefile_content.append(temp_temp_line)

                    temp_temp_temp_makefile_content.append(line_4)
                    continue
            
            # write to a preprocessed file
            # then execute `make` on that file
            # get returned output from that file
            # decides which part of code to be included
            if prepare_for_war:

                # append `$(info "endif")` at the end
                # because there might be some random makefile error after running the makefile
                # using this endif to tell me not to include any outputs that outputs after this `endif` output
                temp_temp_makefile_content.append(temp_temp_line)
                temp_temp_temp_temp_makefile_content = []
                temp_temp_temp_temp_makefile_content = temp_makefile_content.copy()
                temp_temp_temp_temp_makefile_content.extend(temp_temp_makefile_content)

                with open(makefile_preprocessed_path, "w", encoding='utf-8') as file_3:
                    file_3.write(''.join(temp_temp_temp_temp_makefile_content))
                    file_3.flush()
                prepare_for_war = False

                # You have to pass in argument by list
                # eg: 'make' '-f' '/path/to/Makefile' 'target_recipe' 'var=1'
                command = ['make', '-f', makefile_preprocessed_path]
                command.extend(makefile_command)
                process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=os.environ.copy())
                output, error = process.communicate()
                # The error here mainly for debugging purposes only
                # so that i can hover over it to see the value
                error_decoded = error.decode("utf-8")
                error_list = [item[1:-1] + '\n' for item in error_decoded.split('\n')]
                output_decoded = output.decode("utf-8")
                output_list = [item[1:-1] + '\n' for item in output_decoded.split('\n')]
                
                # the last 2 lines, are always
                # last line = new line
                output_list.pop()
                # 2nd last line = `endif` line, sometimes output has only 1 element so need check for null
                if output_list:
                    output_list.pop()

                # from the output_list, given the line number, retain those,
                # the rest, make them into newline
                preserve_line = []
                for output_1 in output_list:
                    line_number_1, line_8 = output_1.split(':', 1)
                    preserve_line.append(int(line_number_1))
                
                list_length = len(temp_makefile_content)

                for index_9, line_9 in enumerate(temp_temp_temp_makefile_content):
                    
                    if preserve_line:
                        offset_length = index_9 + list_length + 1
                        if offset_length == preserve_line[0]:

                            leading_whitespace_length = len(temp_temp_temp_makefile_content[index_9]) - len(temp_temp_temp_makefile_content[index_9].lstrip())
                            temp_temp_temp_makefile_content[index_9] = temp_temp_temp_makefile_content[index_9][:-1]
                            
                            if not is_target_recipe and not is_backward_slash:
                                temp_temp_temp_makefile_content[index_9] = temp_temp_temp_makefile_content[index_9].lstrip()


                            if is_backward_slash:
                                if not temp_temp_temp_makefile_content[index_9].endswith('\\'):
                                    is_backward_slash = False
                                else:
                                    temp_temp_temp_makefile_content[index_9] = temp_temp_temp_makefile_content[index_9] + '\n'

                            elif is_backward_slash == False:
                                # If end if backward slash, cannot add any comment behind
                                # TODO: Now, when wanna restore everthing back, the line that has '\\' at the end will not get the whitespace restored
                                # this will make makefile run fail
                                if temp_temp_temp_makefile_content[index_9].endswith('\\') and not is_target_recipe:
                                    temp_temp_temp_makefile_content[index_9] = '#TO_ADD_BACK_WHITESPACE_BACKWARD_SLASH' + ':' + str(leading_whitespace_length) + '\n' + temp_temp_temp_makefile_content[index_9] + '\n'
                                    is_backward_slash = True
                                elif is_target_recipe:
                                    temp_temp_temp_makefile_content[index_9] = '#TOREMOVE ' + temp_temp_temp_makefile_content[index_9] + '\n'
                                else:
                                    temp_temp_temp_makefile_content[index_9] = temp_temp_temp_makefile_content[index_9] + '#' + str(leading_whitespace_length) + ':TO_ADD_BACK_WHITESPACE\n'


                            preserve_line.pop(0)
                            continue
                    temp_temp_temp_makefile_content[index_9] = '\n'

                temp_makefile_content.extend(temp_temp_temp_makefile_content)
                temp_temp_temp_temp_makefile_content = []
                temp_temp_temp_makefile_content = []
                temp_temp_makefile_content = []
                
                # here set it to False, cause i want anything falls under target_recipe, comment it
                # cos most of the case, `ifeq` that under target_recipe, are mostly command that will execute compile/build/linking
                # which will cause it to fail
                # Update: Due to the fact that, under target_recipe, there's multiple ifeq, multiple endif
                # setting is_target_recipe to false here makes it to not putting `#TOREMOVE ` for the lines that is under target_recipe
                # So, i tied comment it out
                # And then i tried putting variable assignment after target recipe
                # Guess what, it works, the variable is still evaluated, i dk why, but hurray
                # is_target_recipe = False
                continue
            
            if temp_line.startswith('ifeq') or temp_line.startswith('ifneq'):
                has_guarding = True
                temp_temp_makefile_content.append(line_4)
                temp_temp_temp_makefile_content.append(line_4)
                guard_nest_level += 1
            else:
                if re.match(test.target_recipe_regex, line_4):
                    temp_temp_temp_temp_line = '#TOREMOVE ' + line_4
                    temp_makefile_content.append(temp_temp_temp_temp_line)
                    is_target_recipe = True
                elif is_target_recipe:
                    temp_temp_temp_temp_line = '#TOREMOVE ' + line_4
                    temp_makefile_content.append(temp_temp_temp_temp_line)
                else:
                    temp_makefile_content.append(line_4)
        

        # remove all thsoe '#TOREMOVE ' that i put
        make_file_content = temp_makefile_content.copy()
        for index_4, line_6 in enumerate(temp_makefile_content):
            if line_6.startswith('#TOREMOVE '):
                # Remove the sentence, from the front
                make_file_content[index_4] = line_6[len('#TOREMOVE '):]

        temp_makefile_content = make_file_content.copy()
        number_of_whitespace = 0
        # add back all the whitespaces for backward slash case

        # Note:
        # There's no need to claculate list offset,
        # eg:
        # del make_file_content[index_5 - offset_index]
        # offset_index -= 1

        # the content inside will still be in 1 line, like 
        # '#TO_ADD_BACK_WHITESPACE_BACKWARD_SLASH:2\nABC = \\\n'
        make_file_content = temp_makefile_content.copy()
        for index_5, line_7 in enumerate(temp_makefile_content):
            if line_7.startswith('#TO_ADD_BACK_WHITESPACE_BACKWARD_SLASH:'):
                # Remove the sentence, from the front
                temp_temp_temp_temp_temp_line = line_7[len("#TO_ADD_BACK_WHITESPACE_BACKWARD_SLASH:"):]
                number_of_whitespace = int(temp_temp_temp_temp_temp_line[0])
                # Remove the numbers at the beginning of line, and the newline
                temp_temp_temp_temp_temp_line = temp_temp_temp_temp_temp_line[2:]
                for _ in range(number_of_whitespace):
                    temp_temp_temp_temp_temp_line = '\t' + temp_temp_temp_temp_temp_line
                make_file_content[index_5] = temp_temp_temp_temp_temp_line
        temp_makefile_content = make_file_content.copy()

        number_of_whitespace = 0
        # add back all the whitespaces
        make_file_content = temp_makefile_content.copy()
        for index_5, line_7 in enumerate(temp_makefile_content):
            if line_7.endswith('TO_ADD_BACK_WHITESPACE\n'):
                # remove the sentence, from behind
                temp_temp_temp_temp_temp_line = line_7[: - len(":TO_ADD_BACK_WHITESPACE\n")]
                number_of_whitespace = int(temp_temp_temp_temp_temp_line[-1])
                for _ in range(number_of_whitespace):
                    temp_temp_temp_temp_temp_line = '\t' + temp_temp_temp_temp_temp_line
                # Remove the number, and the newline from the end
                temp_temp_temp_temp_temp_line = temp_temp_temp_temp_temp_line[:-2]
                # add back newline
                temp_temp_temp_temp_temp_line += '\n'
                make_file_content[index_5] = temp_temp_temp_temp_temp_line

        # Reset variable
        has_guarding = False
        prepare_for_war = False
        is_target_recipe = False
        lines_2 = []
        temp_makefile_content = []
        temp_temp_makefile_content = []
        temp_temp_temp_makefile_content = []
        temp_temp_temp_temp_makefile_content = []
        guard_nest_level = 0
        temp_line = ''
        temp_temp_line = ''
        temp_temp_temp_line = ''
        temp_temp_temp_temp_line = ''
        temp_temp_temp_temp_temp_line = ''
        temp_temp_temp_temp_temp_temp_line = ''
        command = []
        process = None
        output = None
        error = None
        error_decoded = ''
        error_list = []
        output_decoded = ''
        output_list = []
        index_3 = 0
        output_list_0 = ''
        match_2 = None

    with open(makefile_preprocessed_path, "w", encoding='utf-8') as file_4:
        file_4.write(''.join(make_file_content))
        file_4.flush()













def evaluate_variables(makefile_preprocessed_path):
    # This one do the makefile dictionary
    with open(makefile_preprocessed_path, "r", encoding='utf-8') as file:

        lines = []
        temp_makefile_content = []
        matches = None
        makefile_database_lines = []
        match_string = ''
        string_to_search_for = ''
        makefile_database_file = None
        found = False
        the_value = ''
        stripped_line = ''
        temp_temp_makefile_content = []
        process = None
        output = None
        error = None
        error_decoded = ''
        error_list = []
        output_decoded = ''
        output_list = []
        output_stripped = []
        line_number = 0
        output_to_write = []
        output_to_match_for_the_value = []
        temp_line = ''
        append_path = ''
        current_makefile = ''
        new_makefile_path = ''
        
        temp_temp_temp_temp_temp_temp_temp_temp_line = ''
        is_target_recipe= False

        lines = file.readlines()

        for index, line in enumerate(lines):
            temp_temp_temp_temp_temp_temp_temp_line = line.lstrip()

            # If comment, append ''
            if temp_temp_temp_temp_temp_temp_temp_line.startswith('#'):
                temp_makefile_content.append('')
                continue
            
            # If is within targer_recipe, all the code under target_recipe, append `#TOREMOVE`
            # reason for this is because some code under target_recipe will fail if no target_recipe
            # eg:
            # target_recipe:
            #    compile_code
            
            # Even if i modify makefile to
            # That is, comment target_recipe, and strip leading whitespace of the `compile_code`
            # eg:
            # # COMMENT target_recipe:
            # compile_code

            # It still complains missing `separator, stop.` error
            # TODO: Once is_target_recipe is set to TRUE, there's no return
            # What will happen if you have another variable assignment after the whole target_recipe?
            # Does it still work like that? hmm...
            # Update: I tried to put another variable assignment after the whole target_recipe block, it works
            # The variable is not commented and value is printed. IT WORKS, I DONT KNOW WHY
            if not re.match(test.assigned_variable_regex, line) and line != '\n' and is_target_recipe:
                temp_temp_temp_temp_temp_temp_temp_temp_line = '#TOREMOVE ' + line
                temp_makefile_content.append(temp_temp_temp_temp_temp_temp_temp_temp_line)
            else:
                temp_makefile_content.append(temp_temp_temp_temp_temp_temp_temp_line)


            # To handle target_recipe code, copied from above
            if re.match(test.target_recipe_regex, line):
                temp_temp_temp_temp_temp_temp_temp_temp_line = '#TOREMOVE ' + line
                temp_makefile_content[index] = temp_temp_temp_temp_temp_temp_temp_temp_line
                is_target_recipe = True

            # search for all wrapped variables
            if re.search(test.variable_regex, line):
                matches = re.findall(test.variable_regex, line)
                for match in matches:
                    output_to_write = []

                    # Just wanna make it to write `$(info VAR=$(VAR))`
                    # So when run make, it will print `VAR=value`
                    match_string = match
                    match_string = match_string.replace('${', '').replace('}', '')
                    match_string = match_string.replace('$(', '').replace(')', '')
                    
                    string_to_search_for = match_string + '='
                    
                    makefile_database_file = open(makefile_database_path, "r", encoding='utf-8')
                    # Search weather this variable is existed in the databse
                    makefile_database_file.seek(0)
                    
                    makefile_database_lines = makefile_database_file.readlines()

                    # after reading lines, close the file and reopen again with append mode
                    # for writing operation later
                    makefile_database_file.close()
                    makefile_database_file = open(makefile_database_path, "a", encoding='utf-8')
                    
                    # Search weather this variable existed in database
                    found = False
                    the_value = ''
                    # reason why i put line_2, cos, it will disturb the original `line` that i had above LOL
                    # loop from bottom to top, bottom one are the newest value
                    for line_2 in reversed(makefile_database_lines):
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
                    with open(temp_makefile_path, "w", encoding='utf-8') as file_2:
                        temp_temp_makefile_content = temp_makefile_content.copy()
                        temp_temp_makefile_content.append(f"$(info {match_string}={match})\n")
                        # the content only be written after the file descriptor is closed, well, unless you call file.flush()
                        file_2.write(''.join(temp_temp_makefile_content))

                    # Call a process to execute `make` command, copy my current environment to it
                    command = ['make', '-f', temp_makefile_path]
                    command.extend(makefile_command)
                    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=os.environ.copy())
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
                    output_to_match_for_the_value = output_to_match_for_the_value[len(string_to_search_for):].strip()
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


            # search for all assigned variables
            # code similar to `if re.search(test.variable_regex, line):` above
            # if want understand, look comments over there
            if re.search(test.assigned_variable_regex, line):
                match = re.search(test.assigned_variable_regex, line)

                output_to_write = []

                match_string = match.group()
                # cos my regex matches `=` and `:=`, remove it
                match_string = match_string.replace(':', '').replace('=', '').replace('?', '').replace('+', '')
                # remove all leading & trailing whitespaces
                match_string = match_string.strip()

                wrapped_string = '$(' + match_string + ')'
                
                string_to_search_for = match_string + '='
                
                makefile_database_file = open(makefile_database_path, "r", encoding='utf-8')
                makefile_database_file.seek(0)
                
                makefile_database_lines = makefile_database_file.readlines()

                makefile_database_file.close()
                makefile_database_file = open(makefile_database_path, "a", encoding='utf-8')
                
                found = False
                the_value = ''
                for line_2 in reversed(makefile_database_lines):
                    found = False
                    stripped_line = line_2.split(":")[2]
                    if stripped_line.startswith(string_to_search_for):
                        found = True
                        the_value = line_2[line_2.index(string_to_search_for) + len(string_to_search_for):].strip()
                        break
                
                with open(temp_makefile_path, "w", encoding='utf-8') as file_2:
                    temp_temp_makefile_content = temp_makefile_content.copy()
                    temp_temp_makefile_content.append(f"$(info {match_string}={wrapped_string})\n")
                    file_2.write(''.join(temp_temp_makefile_content))
                
                command = ['make', '-f', temp_makefile_path]
                command.extend(makefile_command)
                process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=os.environ.copy())
                output, error = process.communicate()
                output_stripped = output.decode("utf-8")[:-1]
                output_stripped = output_stripped.split('\n', 1)[0]
                output_stripped = output_stripped.strip()
                line_number = str(index+1)
                output_to_write.append(makefile_path + ':' + line_number + ':' + output_stripped + '\n')
                output_to_match_for_the_value = output_stripped
                output_to_match_for_the_value = output_to_match_for_the_value[len(string_to_search_for):].strip()
                if found:
                    if the_value != output_to_match_for_the_value and \
                        output:
                        makefile_database_file.write(''.join(output_to_write))
                        makefile_database_file.flush()

                else:
                    if output:
                        makefile_database_file.write(''.join(output_to_write))
                        makefile_database_file.flush()
                        

            # search for `include makefile`
            if line.startswith('include'):
                # first, we have to find whether there's variable in the path
                # eg: include ../$(WORKSPACE)/path/to/Makefile
                temp_line = line

                if makefile_database_file:
                    makefile_database_file.close()
                makefile_database_file = open(makefile_database_path, "r", encoding='utf-8')
                makefile_database_lines = makefile_database_file.readlines()
                matches = re.findall(test.variable_regex, line)
                output_to_write = []

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
                makefile_database_file = open(makefile_database_path, "a", encoding='utf-8')
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
                # print(output)
                # print(error)

        make_file_content = []
        makefile_database_file.close()

        lines = []
        temp_makefile_content = []
        matches = None
        makefile_database_lines = []
        match_string = ''
        string_to_search_for = ''
        makefile_database_file = None
        found = False
        the_value = ''
        stripped_line = ''
        temp_temp_makefile_content = []
        process = None
        output = None
        error = None
        error_decoded = ''
        error_list = []
        output_decoded = ''
        output_list = []
        output_stripped = []
        line_number = 0
        output_to_write = []
        output_to_match_for_the_value = []
        temp_line = ''
        append_path = ''
        current_makefile = ''
        new_makefile_path = ''
        
        temp_temp_temp_temp_temp_temp_temp_temp_line = ''
        is_target_recipe= False












def include_handling(makefile_preprocessed_path):
    lines = []
    splits = []
    makefile_include_path = ''
    makefile_current_directory = ''
    makefile_path_2 = ''
    makefile_line_number = 0
    read_data_list = []
    read_data = ''
    read_data_number_of_lines = 0
    write_data = []
    makefile_content = []


    line_trim_leading_whitespace = ''
    include_path = ''
    matches = None
    match_string = ''
    string_to_search_for = ''
    makefile_database_lines = []
    stripped_line = ''

    # `include` handling
    # Why this handling can be done after all those finished
    # because when you run makefile that has `include`, it will still process `include`
    # and the variable you have in your memory is still valid
    # like, when you do $(info VAR) after the `include`, is a valid $VAR
    with open(makefile_preprocessed_path, "r", encoding='utf-8') as file_6:


        with open(makefile_database_path, "r", encoding='utf-8') as file_10:
            makefile_database_lines = file_10.readlines()

        with open(makefile_preprocessed_path, 'r', encoding='utf-8') as file_9:
            write_data = file_9.readlines()

        lines = file_6.readlines()
        for index, line in enumerate(lines):
            line_trim_leading_whitespace = line.lstrip()
            if not line_trim_leading_whitespace.startswith('include'):
                continue

            include_path = line_trim_leading_whitespace

            if include_path.endswith('\n'):
                include_path = include_path[:-1]

            include_path = include_path[len('include'):]
            include_path = include_path.lstrip()

            matches = re.findall(test.variable_regex, include_path)
            for match in matches:
                match_string = match
                match_string = match_string.replace('${', '').replace('}', '')
                match_string = match_string.replace('$(', '').replace(')', '')
                string_to_search_for = match_string + '='
            
                for line_3 in makefile_database_lines:
                    stripped_line = line_3.split(":")[2]
                    if stripped_line.startswith(string_to_search_for):
                        the_value = line_3[line_3.index(string_to_search_for) + len(string_to_search_for):].strip()
                        include_path = include_path.replace(match, the_value)
                        break

            # Now, this is getting the path `/data/myrepo/trbo/gemstones/gemstones/preston_utils_makefile_output/makefile_preprocessed.mk`
            # So, make it `/data/myrepo/trbo/gemstones/gemstones`
            # If you run my script, i will always places `makefile_preprocess.mk` in a folder `preston_utils_makefile_output`
            # so this hardcoded path finding works
            makefile_current_directory = makefile_preprocessed_path.rsplit('/', 2)[0]

            # change the current working directory
            # so that, if the include is using relative path like `../a/b/c` also can open.
            os.chdir(makefile_current_directory)
            with open(include_path, 'r', encoding='utf-8') as file_7:
                read_data_list = file_7.readlines()
                read_data = ''.join(read_data_list)

            write_data[index] = '#MAKEFILE_INCLUDE ' + write_data[index]
            write_data[index] = write_data[index] + read_data
            write_data[index] = write_data[index] + '\n#END_MAKEFILE_INCLUDE\n'
            
            
        with open(makefile_with_include_path, 'w', encoding='utf-8') as file_8:
            file_8.write(''.join(write_data))
            file_8.flush()


def main():
    has_include = False
    has_guarding = False
    read_data = []
    line_trim_leading_whitespace = ''

    preprocess(makefile_path, makefile_preprocessed_path)
    evaluate_variables(makefile_path)
    include_handling(makefile_preprocessed_path)
    preprocess(makefile_preprocessed_path, makefile_preprocessed_path)
    evaluate_variables(makefile_with_include_path)

    with open(makefile_preprocessed_path, 'r', encoding='utf-8') as file_5:
        read_data = file_5.readlines()

    for line_5 in read_data:
        line_trim_leading_whitespace = line_5.lstrip()
        if line_trim_leading_whitespace.startswith('include'):
            has_include = True

        if line_trim_leading_whitespace.startswith('ifeq') or \
            line_trim_leading_whitespace.startswith('ifneq'):
            has_guarding = True
        
        if has_include and has_guarding:
            break



    while has_include  or \
        has_guarding:

        if has_guarding:
            preprocess(makefile_with_include_path, makefile_with_include_path)
            evaluate_variables(makefile_with_include_path)

        if has_include:
            include_handling(makefile_with_include_path)
            evaluate_variables(makefile_with_include_path)


        has_include = False
        has_guarding = False

        with open(makefile_with_include_path, 'r', encoding='utf-8') as file_5:
            read_data = file_5.readlines()

        for line_5 in read_data:
            line_trim_leading_whitespace = line_5.lstrip()
            if line_trim_leading_whitespace.startswith('include'):
                has_include = True

            if line_trim_leading_whitespace.startswith('ifeq') or \
                line_trim_leading_whitespace.startswith('ifneq'):
                has_guarding = True
            
            if has_include or has_guarding:
                break




main()
# remove files at the end of script
os.remove(temp_makefile_path)
print(f"Output: {makefile_preprocessed_path}")
print(f"Output: {makefile_database_path}")
print(f"Output: {makefile_with_include_path}")
print("Script Ends")