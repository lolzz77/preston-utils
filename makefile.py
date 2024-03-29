import sys
import re
import subprocess
import os
import shutil
import subprocess

if len(sys.argv) != 2:
    print("Invalid number of arguments. Usage: python makefile.py <makefile_path>")
    sys.exit(1)

makefile_path = sys.argv[1]
current_path = os.getcwd()

makefile_python_output_path = current_path + '/makefile_python_output'

if not os.path.exists(makefile_python_output_path):
    os.makedirs(makefile_python_output_path)

makefile_database_path = makefile_python_output_path + '/makefile_database.txt'
temp_makefile_path = makefile_python_output_path + '/temp_makefile.mk'

temp_makefile_content = ""

# Matches ${...}, $(...)
variable_regex = r'\$[\(\{][a-zA-Z0-9_-]+[\)\}]'

makefile_database_file = open(makefile_database_path, "w")

try:
    # Open the main makefile that you're going to put your build command into
    with open(makefile_path, "r") as file:
        lines = file.readlines()
        for index, line in enumerate(lines):
            temp_makefile_content += line

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
                        stripped_line = line_2.split(":")[1]
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
                        temp_temp_makefile_content = temp_makefile_content
                        temp_temp_makefile_content += f"$(info {match_string}={match})\n"
                        # the content only be written after the file descriptor is closed, well, unless you call file.flush()
                        file_2.write(temp_temp_makefile_content)

                    # Call a process to execute `make` command, copy my current environment to it
                    process = subprocess.Popen(['make', '-f', temp_makefile_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=os.environ.copy())
                    # Example output
                    # Output : b'<the value of {match}\n'
                    # error : make: *** no targets. Stop.\n'
                    # the `b` infront, is not count in the character, it basically means it is displaying in binrary format i guess
                    output, error = process.communicate()
                    # this is to remove '\n' at the end
                    output_stripped = output.decode("utf-8")[:-1]
                    output_to_write = str(index+1) + ':' + output_stripped + '\n'

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
                            makefile_database_file.write(output_to_write)
                            makefile_database_file.flush()

                    else:
                        # else, write into database
                        # only write when `output` has something
                        if output:
                            makefile_database_file.write(output_to_write)
                            makefile_database_file.flush()
                        
            # search for included makefile
            if line.startswith('include'):
                # no need + '\n', the `line` already included it
                # if you put, above code will error out of index when doing stripping
                output_to_write = str(index + 1) + ':' + line
                makefile_database_file.write(output_to_write)
                makefile_database_file.flush()

                # line = include ../path/to/directory\n
                # strip `include`, leading whitespace, and the '\n'
                # no need check whether the path contains name.mk or not, it still works for command `make -f /dir/`
                append_path = line.strip('include').strip().rstrip('\n')
                # get the path of the current opened makefile
                # strip `makefile` from the string, append the path of the `line` into it
                current_makefile = makefile_path
                if current_makefile.endswith("Makefile"):
                    current_makefile = current_makefile[:-8]
                new_makefile_path = current_makefile + append_path
                process = subprocess.Popen(['make', '-f', new_makefile_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=os.environ.copy())
                output, error = process.communicate()
                print(output)
                print(error)
except FileNotFoundError:
    print("File not found.")
except IOError:
    print("Error reading the file.")


makefile_database_file.close()
print("Script Ends")