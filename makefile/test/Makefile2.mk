

ifeq ($(VAR1), 1)
	ifeq ($(VAR1), 1)
		CMD = \
			ABC/DEF
	else
		CMD = \
			QWE/ASD
	endif
else
	ifeq ($(VAR2), 2)
		ifeq ($(VAR2), 2)
			CMD = \
				CXZ/DSA
		else
			CMD = \
				EWQ/DSA
		endif
	else ifeq ($(VAR2), 3)
		CMD = \
			GFD/ERT
	else
		ifeq ($(VAR2), 4)
			CMD = \
				ABC/DEF
		else
			CMD = \
				POI/LKJ
		endif
	endif
endif



CMD2 = \
	-I"$(VAR1)/a" \
	-l"$(VAR1)/b.lib"

ifeq ($(VAR1), 1)
	CMD2+=-l"$(VAR1)/$(VAR1)"
else
	CMD2+=-l"$(VAR2)"
endif

ifeq ($(VAR1), 1)
CMD3 += \
	-l"$(VAR1)/a.a" \
	-l"$(VAR1)/b.a" \
	-l"$(VAR1)/c.a"
endif


all: $(VAR1) $(VAR2) 
$(VAR2): $(VAR3)
	-@echo build
	$(VAR4) -q -b -o $@ $<
	-@echo pack
ifeq ($(VAR1), 1)
	mv $(VAR2) $(VAR2)_TEMP
	cd $(VAR1); \
	chmod 755 abc; \
	./abc -param=123
	cd $(VAR1)/a;
else
	$(VAR2) /123
	-@echo Create
endif

$(VAR3): $(VAR4)

ifeq ($(VAR1), 1)
	-@echo -z -q -a -c -m"$(VAR1)" -o"$@" -w -x > $(VAR2)
else
	-@echo --abc -z -q -a -c -m"$(VAR1)" -o"$@" -w -x > $(VAR2)
endif
	-@echo a
	-@echo b
	-@echo c

$(VAR1)/$(VAR2): $(ABC)
	@echo compiling

vpath %.cpp $(foreach src, $(VAR1), $(dir $(VAR1)))
vpath %.obj $(VAR1)

