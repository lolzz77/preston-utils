# command
# make [target]
# if you want enable -DDEBUG
# make [target] f={any value}


# -g option so you can use GDB on generated output file
# ${f}, f stands for flag
# $(FLAG) is for whether u want to define -DDEBUG or not, this is for #ifdef DEBUG in the coding
# -o = output name

# GDB guide
# gdb ./allFileExe
# b [breakpoint]
# r [repo name]

# check if user pass any value to 'f'
ifeq ($(f),)
    # if no pass 'f' variable value, then set FLAG to empty string
	FLAG =
else
    # if any value is passed to 'f', then set FLAG to -DDEBUG
	FLAG = -DDEBUG
endif

# if you have multiple include in one line, write like this
# INC=-I/usr/informix/incl/c++ -I/opt/informix/incl/public
# no need "/" or "\" at start, straight away put dir name
# INC=-Idir
# should you have subdir in dir, only then u put "/"
# INC=-Idir/subdir
# if your header is in same dir as your source file, then actually u dont need to specify -I
# but if you want also can, doesn't matter

# headers to include
# NULL for the moment
INC = 

# warning
# null for the moment
WAR = 

CC = gcc
CFLAGS = -g

# Ref: https://begriffs.com/posts/2020-03-23-concurrent-programming.html#our-first-concurrent-program
# This is generic make command
# run `make [filename] without the extension` to make the executable output
.c:
	$(CC) $(CFLAGS) $(WAR) $(INC) -o $@ $<

# .PHONY: allFile fewFile reset oneFile allFileSem regexChecker allFileFewFunc

# all: allFunc callerFunc semaphore

# # append log on all files in repo
# allFunc:
# 	gcc -g $(WAR) $(INC) -o allFuncExe allFunc.c $(FLAG)

# # Write log to caller functions
# callerFunc:
# 	gcc -g $(WAR) $(INC) -o callerFuncExe callerFunc.c $(FLAG)

# # all files, but is for logging vr_capture_semevent
# semaphore:
# 	gcc -g $(WAR) $(INC) -o semaphoreExe semaphore.c $(FLAG)

# # run git reset --hard HEAD on all dir
# reset:
# 	gcc -g $(WAR) $(INC) -o resetExe reset.c $(FLAG)

# # to test regex
# regexChecker:
# 	gcc -g $(WAR) $(INC) -o regexCheckerExe regexChecker.c $(FLAG)
