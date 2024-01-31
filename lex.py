# Prerequisite
# pip install pathlib

import include
import glob
import os
import sys
from pathlib import Path
import re
import subprocess
from enum import Enum

# input in temrinal:
# run command:
# 'python allFileMakefile.py repo'
# then when u put this code 'print(len(sys.argv))'
# will output 2

# this means, only run this if this file is directly called from terminal
# not from imported module
if __name__ == "__main__":
	if(len(sys.argv) < 2):
		print("Wrong argument. Terminating script.")
		sys.exit()

	dir_list = []
	dir_list.append(sys.argv[1])



class CPPType(Enum):
	CPP_NONE			= 0
	CPP_WHITESPACE 		= 1
	CPP_NEWLINE 		= 2
	CPP_NUMBER 			= 3
	CPP_NAME 			= 4
	CPP_STRING_SINGLE_QUOTE = 5
	CPP_STRING_DOUBLE_QUOTE = 6
	CPP_MULTILINE_COMMENT 	= 7
	CPP_SINGLE_LINE_COMMENT	= 8
	CPP_DIV_EQ			= 9
	CPP_DIV				= 10
	CPP_LESS			= 11
	CPP_LESS_EQ			= 12
	CPP_SPACESHIP		= 13
	CPP_LSHIFT_EQ		= 14
	CPP_LSHIFT			= 15
	CPP_OPEN_SQUARE		= 16
	CPP_OPEN_BRACE		= 17
	CPP_GREATER			= 18
	CPP_GREATER_EQ		= 19
	CPP_RSHIFT_EQ		= 20
	CPP_RSHIFT			= 21
	CPP_MOD				= 22
	CPP_MOD_EQ			= 23
	CPP_HASH			= 24
	CPP_PASTE			= 25
	CPP_CLOSE_BRACE		= 26
	CPP_DOT				= 27
	CPP_ELLIPSIS		= 28
	CPP_DOT_STAR		= 29
	CPP_PLUS			= 30
	CPP_PLUS_PLUS		= 31
	CPP_PLUS_EQ			= 32
	CPP_MINUS			= 33
	CPP_DEREF			= 34
	CPP_DEREF_STAR		= 35
	CPP_MINUS_MINUS		= 36
	CPP_MINUS_EQ		= 37
	CPP_AND				= 38
	CPP_AND_AND			= 39
	CPP_AND_EQ			= 40
	CPP_OR				= 41
	CPP_OR_OR			= 42
	CPP_OR_EQ			= 43
	CPP_COLON			= 44
	CPP_SCOPE			= 45
	CPP_CLOSE_SQUARE	= 46
	CPP_MULT_EQ			= 47
	CPP_MULT			= 48
	CPP_EQ_EQ			= 49
	CPP_EQ				= 50
	CPP_NOT_EQ			= 51
	CPP_NOT				= 52
	CPP_XOR_EQ			= 53
	CPP_XOR				= 54
	CPP_QUERY			= 55
	CPP_COMPL			= 56
	CPP_COMMA			= 57
	CPP_OPEN_PAREN		= 58
	CPP_CLOSE_PAREN		= 59
	CPP_SEMICOLON		= 60
	CPP_OTHER			= 61

class CPP_Flag(Enum):
	"""
	flags should be bit-wised
	1 = 0001
	2 = 0010
	4 = 0100
	8 = 1000
	and so on
	"""
	NONE 		= 1
	DIGRAPH 	= 2

class CPPOption(Enum):
	NONE		= 0
	DIGRAPHS	= 1
	C_PLUS_PLUS	= 2
	SCOPE		= 3



def lex(c, string, cpp_option):
	"""
	c 	- the current single character
	string 	- the full string, after the 'c' parameter
		- eg: full string = 'int main()'
		- c = 'm'
		- then, s = 'ain()'
		- this full string is needed cos some CPPType need to check next char to decide
		- so far, only need 2 next char, so, maybe u can pass in maximum of length 3 of 's' parameter
	cpp_option - the compiling option (eg: compile trigraph? compile as CPP? etc)
	"""

	# This is for if u lex-ed more than 1 character, for example, '!='
	# this means, the 1st char & 2nd char are lex-ed, and can skip
	# update: this should be handled by caller

	result = {}
	result['char'] = c
	result['flag'] = CPP_Flag.NONE
	result['type'] = CPPType.CPP_NONE
	next_char = ''
	next_next_char = ''
	next_next_next_char = ''

	if len(string) > 1:
		next_char = string[1]

	if len(string) > 2:
		next_next_char = string[2]

	if len(string) > 3:
		next_next_next_char = string[3]

	if c in [' ', '\t', '\f', '\v', '\0']:
		result['type'] = CPPType.CPP_WHITESPACE

	elif c == '\n':
		result['type'] = CPPType.CPP_NEWLINE
		pass

	elif c in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
		result['type'] = CPPType.CPP_NUMBER

	elif c in ['L', 'u', 'U', 'R']:
		pass

	elif c in [
			'_',
			# Note: 'U' is not included here
			'a', 'b', 'c', 'd', 'e', 'f',
			'g', 'h', 'i', 'j', 'k', 'l',
			'm', 'n', 'o', 'p', 'q', 'r',
			's', 't',      'v', 'w', 'x',
			'y', 'z',
			# Note: 'L', 'R', 'U' is not included here
			'A', 'B', 'C', 'D', 'E', 'F',
			'G', 'H', 'I', 'J', 'K',
			'M', 'N', 'O', 'P', 'Q',
			'S', 'T',      'V', 'W', 'X',
			'Y', 'Z'
		]:
		result['type'] = CPPType.CPP_NAME

	elif c in ['\'', '"']:
		result['type'] = {
			'\'': CPPType.CPP_STRING_SINGLE_QUOTE,
			'"': CPPType.CPP_STRING_DOUBLE_QUOTE
		}[c] # this is like dictionary, given key, return the value
		pass

	elif c == '/':
		if next_char == '*':
			result['type'] = CPPType.CPP_MULTILINE_COMMENT
		elif next_char == '/':
			result['type'] = CPPType.CPP_SINGLE_LINE_COMMENT
		elif next_char == '=':
			result['type'] = CPPType.CPP_DIV_EQ
		else:
			result['type'] = CPPType.CPP_DIV

	elif c == '<':
		result['type'] = CPPType.CPP_LESS
		if next_char == '=':
			result['type'] = CPPType.CPP_LESS_EQ
			if next_next_char == '>':
				result['type'] = CPPType.CPP_SPACESHIP
		elif next_char == '<':
			if next_next_char == '=':
				result['type'] = CPPType.CPP_LSHIFT_EQ
			else:
				result['type'] = CPPType.CPP_LSHIFT
		elif cpp_option == CPPOption.DIGRAPHS:
			if next_char == ':':
				result['flags'] |= CPP_Flag.DIGRAPH
				result['type'] = CPPType.CPP_OPEN_SQUARE
			elif next_char == '%':
				result['flags'] |= CPP_Flag.DIGRAPH
				result['type'] = CPPType.CPP_OPEN_BRACE

	elif c == '>':
		result['type'] = CPPType.CPP_GREATER
		if next_char == '=':
			result['type'] = CPPType.CPP_GREATER_EQ
		elif next_char == '>':
			if next_next_char == '=':
				result['type'] = CPPType.CPP_RSHIFT_EQ
			else:
				result['type'] = CPPType.CPP_RSHIFT

	elif c == '%':
		result['type'] = CPPType.CPP_MOD
		if next_char == '=':
			result['type'] = CPPType.CPP_MOD_EQ
		elif cpp_option == CPPOption.DIGRAPHS:
			if next_char == ':':
				result['flags'] |= CPP_Flag.DIGRAPH
				result['type'] = CPPType.CPP_HASH
				# This means double hash, 
				# `%:` = #, `%:%:` = ##
				# Double hash = CPP_PASTE
				if next_next_char == '%' and next_next_next_char == ':':
					result['type'] = CPPType.CPP_PASTE
			elif next_char == '>':
				result['flags'] |= CPP_Flag.DIGRAPH
				result['type'] = CPPType.CPP_CLOSE_BRACE

	elif c == '.':
		result['type'] = CPPType.CPP_DOT
		if next_char.isdigit():
			result['type'] = CPPType.CPP_NUMBER
		elif next_char == '.' and next_next_char == '.':
			result['type'] = CPPType.CPP_ELLIPSIS
		elif next_char == '*' and cpp_option == CPPOption.C_PLUS_PLUS:
			result['type'] = CPPType.CPP_DOT_STAR

	elif c == '+':
		result['type'] = CPPType.CPP_PLUS
		if next_char == '+':
			result['type'] = CPPType.CPP_PLUS_PLUS
		elif next_char == '=':
			result['type'] = CPPType.CPP_PLUS_EQ

	elif c == '-':
		result['type'] = CPPType.CPP_MINUS
		if next_char == '>':
			result['type'] = CPPType.CPP_DEREF
			if next_next_char == '*' and cpp_option == CPPOption.C_PLUS_PLUS:
				result['type'] = CPPType.CPP_DEREF_STAR
		elif next_char == '-':
			result['type'] = CPPType.CPP_MINUS_MINUS
		elif next_char == '=':
			result['type'] = CPPType.CPP_MINUS_EQ

	elif c == '&':
		result['type'] = CPPType.CPP_AND
		if next_char == '&':
			result['type'] = CPPType.CPP_AND_AND
		elif next_char == '=':
			result['type'] = CPPType.CPP_AND_EQ

	elif c == '|':
		result['type'] = CPPType.CPP_OR
		if next_char == '|':
			result['type'] = CPPType.CPP_OR_OR
		elif next_char == '=':
			result['type'] = CPPType.CPP_OR_EQ

	elif c == ':':
		result['type'] = CPPType.CPP_COLON
		if next_char == ':' and cpp_option == CPPOption.SCOPE:
			result['type'] = CPPType.CPP_SCOPE
		elif next_char == '>' and cpp_option == CPPOption.DIGRAPHS:
			result['flags'] |= CPP_Flag.DIGRAPH
			result['type'] = CPPType.CPP_CLOSE_SQUARE

	elif c == '*':
		if next_char == '=':  # assuming buffer is a list-like object and cur is the current index
			result['type'] = CPPType.CPP_MULT_EQ
		else:
			result['type'] = CPPType.CPP_MULT

	elif c == '=':
		if next_char == '=':
			result['type'] = CPPType.CPP_EQ_EQ
		else:
			result['type'] = CPPType.CPP_EQ

	elif c == '!':
		if next_char == '=':
			result['type'] = CPPType.CPP_NOT_EQ
		else:
			result['type'] = CPPType.CPP_NOT

	elif c == '^':
		if next_char == '=':
			result['type'] = CPPType.CPP_XOR_EQ
		else:
			result['type'] = CPPType.CPP_XOR

	elif c == '#':
		if next_char == '#':
			result['type'] = CPPType.CPP_PASTE
		else:
			result['type'] = CPPType.CPP_HASH

	elif c in ['?', '~', ',', '(', ')', '[', ']', '{', '}', ';']:
		result['type'] = {
			'?': CPPType.CPP_QUERY,
			'~': CPPType.CPP_COMPL,
			',': CPPType.CPP_COMMA,
			'(': CPPType.CPP_OPEN_PAREN,
			')': CPPType.CPP_CLOSE_PAREN,
			'[': CPPType.CPP_OPEN_SQUARE,
			']': CPPType.CPP_CLOSE_SQUARE,
			'{': CPPType.CPP_OPEN_BRACE,
			'}': CPPType.CPP_CLOSE_BRACE,
			';': CPPType.CPP_SEMICOLON
		}[c] # this is like dictionary, given key, return the value

	else:
		result['type'] = CPPType.CPP_OTHER


	return result


def lex_string(string, cpp_option):
	"""
	Lex a string, under this function,
	it will lex each token.
	"""
	arr_arr = []
	for i, char in enumerate(string):
		temp_string = string[i:]
		arr = lex(char, temp_string, cpp_option)
		arr_arr.append(arr)

	# return arr_arr

	print()
	print(string)
	for arr in arr_arr:
		print(arr)

def decide():
	"""
	Given result from lex_string
	This function decides what kind of syntaxes the string is
	eg: string = int main(){}
	syntaxes = function definition

	eg2: #include <stdio.h>
	stntaxes = include

	+1 char
	CPP_MULTILINE_COMMENT
	CPP_SINGLE_LINE_COMMENT
	CPP_DIV_EQ
	CPP_LESS_EQ
	CPP_LSHIFT
	CPP_GREATER_EQ
	CPP_RSHIFT
	CPP_MOD_EQ
	CPP_NUMBER
	CPP_DOT_STAR
	CPP_PLUS_PLUS
	CPP_PLUS_EQ
	CPP_DEREF
	CPP_MINUS_MINUS
	CPP_MINUS_EQ
	CPP_AND_AND
	CPP_AND_EQ
	CPP_OR_OR
	CPP_OR_EQ
	CPP_SCOPE
	CPP_MULT_EQ
	CPP_EQ_EQ
	CPP_NOT_EQ
	CPP_XOR_EQ
	CPP_PASTE

	+2 char
	CPP_SPACESHIP
	CPP_LSHIFT_EQ
	CPP_RSHIFT_EQ
	CPP_ELLIPSIS
	CPP_DEREF_STAR
	"""