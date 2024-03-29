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

makefile_database_file = open(makefile_database_path, "a+")

try:
    # Open the main makefile that you're going to put your build command into
    with open(makefile_path, "r") as file:
        lines = file.readlines()
        for line in lines:
            temp_makefile_content += line

            # search for all variables
            if re.search(variable_regex, line):
                matches = re.findall(variable_regex, line)
                for match in matches:
                    # Search weather this variable is existed in the databse
                    makefile_database_file.seek(0)

                    match_string = match
                    match_string = match_string.replace('${', '').replace('}', '')
                    match_string = match_string.replace('$(', '').replace(')', '')
                    
                    # TODO : in some cases, there's 
                    # if[$(OS)==WINDOW] PATH=a, else PATH=b
                    # How you gonna handle that?
                    string_to_search_for = match_string + '='
                    
                    makefile_database_lines = makefile_database_file.readlines()
                    
                    found = False
                    for line in makefile_database_lines:
                        found = False
                        if line.startswith(string_to_search_for):
                            found = True
                            break

                    if found:
                        pass
                    else:
                        # else, write the content to temporary makefile
                        # then, execute `make` to run the makefile to print out / evaluates the variable value
                        with open(temp_makefile_path, "w") as file:
                            temp_temp_makefile_content = temp_makefile_content
                            temp_temp_makefile_content += f"$(info {match_string}={match})\n"
                            # the content only be written after the file descriptor is closed, well, unless you call file.flush()
                            file.write(temp_temp_makefile_content)
                        
                        # Call a process to execute `make` command, copy my current environment to it
                        process = subprocess.Popen(['make', '-f', temp_makefile_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=os.environ.copy())
                        # Example output
                        # Output : b'<the value of {match}\n'
                        # error : make: *** no targets. Stop.\n'
                        # the `b` infront, is not count in the character, it basically means it is displaying in binrary format i guess
                        output, error = process.communicate()
                        output_to_write = output.decode("utf-8")[:-1] + '\n'
                        makefile_database_file.write(output_to_write)
                        makefile_database_file.flush()
                            
            # search for included makefile
            # if line.startswith('include'):
            #     print(line)
except FileNotFoundError:
    print("File not found.")
except IOError:
    print("Error reading the file.")


makefile_database_file.close()
print("Script Ends")