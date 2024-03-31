# Makefile Dictionary Utility

# What
![image](./resources/1.png)

![image](./resources/2.png)

TL;DR
1. This script will generate 2 files
- Preprocessed file (all guarding such as `ifeq` will be evaluated & decide which part of code to be included)
- Database file (all those variables value will be printed out)
2. Output will be generated in the `preston_utils_makefile_output` in the current directory that you executed this script

# How to use
1. Run command `python3 [path to this makefile.py script] [path to your Makefile] ["the makefile command you have to pass, with DOUBLE QUOTE!"]`