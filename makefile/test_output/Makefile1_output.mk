# Unit Test runs this command with param VAR1=1
# Start
export PATH:=A

	export PATH:=B



      # Test skip line
include /Makefile1.mk





	export E := E
	include ../dummy_include/dummy_include.mk


F = F1
F := F2
F += F3
G = G
H = H

I = $(F) $(G) $(H)
I_G = $(F) $(G) $(H)

AA = $($(VAR2)_)
HELP = \
	ABC \
	DEF \
	GHI \
	JKL \
 
.PHONY = TARGETA TARGETB
TARGETA: TARGETB

	echo "1"




TARGETB:

	echo "A"





TARGETC: 









		echo "A3"







HELP:
	echo "1"
	@echo "2"
	echo "3"
