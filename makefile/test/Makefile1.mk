# Unit Test runs this command with param VAR1=1
# Start
export PATH:=A
ifeq ($(VAR1),1)
	export PATH:=B
else
	export PATH:=C
endif
      # Test skip line
include /Makefile1.mk

ifneq (,$(findstring windows,$(call lc,$(PATH))))
	D := D
	include /dummy_include/dummy_include.mk
else
	export E := E
	include ../dummy_include/dummy_include.mk
endif

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
ifneq (, $(filter $(VAR1), 1 ))
	echo "1"
else
	echo "2"
endif

TARGETB:
ifneq (, $(filter $(VAR1), 1 ))
	echo "A"
else
	echo "B"
endif


TARGETC: 
ifneq (, $(filter $(VAR1), 1 ))
	ifneq (, $(filter $(VAR2), 1 ))
		ifneq (, $(filter $(VAR3), 1))
			echo "A1"
		endif
	endif
	ifeq "$(VAR4)" "VAR4"
		echo "A2"
	else
		echo "A3"
	endif
else
	echo "A4"
endif 



HELP:
	echo "1"
	@echo "2"
	echo "3"
