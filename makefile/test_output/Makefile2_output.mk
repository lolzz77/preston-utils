# Unit Test runs this command with param VAR1=1



		CMD = \
			ABC/DEF




























CMD2 = \
	-I"$(VAR1)/a" \
	-l"$(VAR1)/b.lib"


	CMD2+=-l"$(VAR1)/$(VAR1)"





CMD3 += \
	-l"$(VAR1)/a.a" \
	-l"$(VAR1)/b.a" \
	-l"$(VAR1)/c.a"


all: $(VAR1) $(VAR2) 
$(VAR2): $(VAR3)
	-@echo build
	$(VAR4) -q -b -o $@ $<
	-@echo pack

	mv $(VAR2) $(VAR2)_TEMP
	cd $(VAR1); \
	chmod 755 abc; \
	./abc -param=123
	cd $(VAR1)/a;





$(VAR3): $(VAR4)


	-@echo -z -q -a -c -m"$(VAR1)" -o"$@" -w -x > $(VAR2)



	-@echo a
	-@echo b
	-@echo c

$(VAR1)/$(VAR2): $(ABC)
	@echo compiling

vpath %.cpp $(foreach src, $(VAR1), $(dir $(VAR1)))
vpath %.obj $(VAR1)

