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
	CPP_GREATER_EQ		= 18
	CPP_RSHIFT_EQ		= 19
	CPP_RSHIFT			= 20
	CPP_MOD				= 21
	CPP_MOD_EQ			= 22
	CPP_HASH			= 23
	CPP_PASTE			= 24
	CPP_CLOSE_BRACE		= 25
	CPP_DOT				= 26
	CPP_ELLIPSIS		= 27
	CPP_DOT_STAR		= 28
	CPP_PLUS			= 29
	CPP_PLUS_PLUS		= 30
	CPP_PLUS_EQ			= 31
	CPP_MINUS			= 32
	CPP_DEREF			= 33
	CPP_DEREF_STAR		= 34
	CPP_MINUS_MINUS		= 35
	CPP_MINUS_EQ		= 36
	CPP_AND				= 37
	CPP_AND_AND			= 38
	CPP_AND_EQ			= 39
	CPP_OR				= 40
	CPP_OR_OR			= 41
	CPP_OR_EQ			= 42
	CPP_COLON			= 43
	CPP_SCOPE			= 44
	CPP_CLOSE_SQUARE	= 45
	CPP_MULT_EQ			= 46
	CPP_MULT			= 47
	CPP_EQ_EQ			= 48
	CPP_EQ				= 49
	CPP_NOT_EQ			= 50
	CPP_NOT				= 51
	CPP_XOR_EQ			= 52
	CPP_XOR				= 53
	CPP_QUERY			= 54
	CPP_COMPL			= 55
	CPP_COMMA			= 56
	CPP_OPEN_PAREN		= 57
	CPP_CLOSE_PAREN		= 58
	CPP_SEMICOLON		= 59
	CPP_OTHER			= 60

class CPP_Flag(Enum):
	NONE 		= 0
	DIGRAPH 	= 1

class CPPOption(Enum):
	"""
	flags should be bit-wised
	1 = 0001
	2 = 0010
	4 = 0100
	8 = 1000
	and so on
	"""
	NONE		= 0
	DIGRAPHS	= 1
	C_PLUS_PLUS	= 2
	SCOPE		= 4




def lex(c, s, cpp_option):
	"""
	c 	- the current single character
	s 	- the full string, after the 'c' parameter
		- eg: full string = 'int main()'
		- c = 'm'
		- then, s = 'ain()'
		- this full string is needed cos some CPPType need to check next char to decide
		- so far, only need 2 next char, so, maybe u can pass in maximum of length 3 of 's' parameter
	cpp_option - the compiling option (eg: compile trigraph? compile as CPP? etc)
	"""
	result = {}
	result['flag'] = CPP_Flag.NONE
	result['type'] = CPPType.CPP_NONE

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
		next_char = s[1]
		if next_char == '*':
			result['type'] = CPPType.CPP_MULTILINE_COMMENT
		elif next_char == '/':
			result['type'] = CPPType.CPP_SINGLE_LINE_COMMENT
		elif next_char == '=':
			result['type'] = CPPType.CPP_DIV_EQ
		else:
			result['type'] = CPPType.CPP_DIV

	elif c == '<':
		next_char = s[1]
		result['type'] = CPPType.CPP_LESS
		if next_char == '=':
			result['type'] = CPPType.CPP_LESS_EQ
			if next_char == '>':
				result['type'] = CPPType.CPP_SPACESHIP
		elif next_char == '<':
			if next_char == '=':
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
		next_char = s[1]
		result['type'] = 'CPP_GREATER'
		if next_char == '=':
			result['type'] = CPPType.CPP_GREATER_EQ
		elif next_char == '>':
			if next_char == '=':
				result['type'] = CPPType.CPP_RSHIFT_EQ
			else:
				result['type'] = CPPType.CPP_RSHIFT

	elif c == '%':
		next_char = s[1]
		next_next_char = s[2]
		result['type'] = CPPType.CPP_MOD
		if next_char == '=':
			result['type'] = CPPType.CPP_MOD_EQ
		elif cpp_option == CPPOption.DIGRAPHS:
			if next_char == ':':
				result['flags'] |= CPP_Flag.DIGRAPH
				result['type'] = CPPType.CPP_HASH
				if next_char == '%' and next_next_char == ':':
					result['type'] = CPPType.CPP_PASTE
					result['val']['token_no'] = 0  # assuming result['val'] is a dictionary
			elif next_char == '>':
				result['flags'] |= CPP_Flag.DIGRAPH
				result['type'] = CPPType.CPP_CLOSE_BRACE

	elif c == '.':
		next_char = s[1]
		next_next_char = s[2]
		result['type'] = CPPType.CPP_DOT
		if next_char.isdigit():
			result['type'] = CPPType.CPP_NUMBER
		elif next_char == '.' and next_next_char == '.':
			result['type'] = CPPType.CPP_ELLIPSIS
		elif next_char == '*' and CPPOption.C_PLUS_PLUS:
			result['type'] = CPPType.CPP_DOT_STAR

	elif c == '+':
		next_char = s[1]
		result['type'] = CPPType.CPP_PLUS
		if next_char == '+':
			result['type'] = CPPType.CPP_PLUS_PLUS
		elif next_char == '=':
			result['type'] = CPPType.CPP_PLUS_EQ

	elif c == '-':
		next_char = s[1]
		result['type'] = CPPType.CPP_MINUS
		if next_char == '>':
			result['type'] = CPPType.CPP_DEREF
			if next_char == '*' and CPPOption.C_PLUS_PLUS:
				result['type'] = CPPType.CPP_DEREF_STAR
		elif next_char == '-':
			result['type'] = CPPType.CPP_MINUS_MINUS
		elif next_char == '=':
			result['type'] = CPPType.CPP_MINUS_EQ

	elif c == '&':
		next_char = s[1]
		result['type'] = CPPType.CPP_AND
		if next_char == '&':
			result['type'] = CPPType.CPP_AND_AND
		elif next_char == '=':
			result['type'] = CPPType.CPP_AND_EQ

	elif c == '|':
		next_char = s[1]
		result['type'] = CPPType.CPP_OR
		if next_char == '|':
			result['type'] = CPPType.CPP_OR_OR
		elif next_char == '=':
			result['type'] = CPPType.CPP_OR_EQ

	elif c == ':':
		next_char = s[1]
		result['type'] = CPPType.CPP_COLON
		if next_char == ':' and CPPOption.SCOPE:
			result['type'] = CPPType.CPP_SCOPE
		elif next_char == '>' and CPPOption.DIGRAPHS:
			result['flags'] |= CPP_Flag.DIGRAPH
			result['type'] = CPPType.CPP_CLOSE_SQUARE

	elif c == '*':
		next_char = s[1]
		if next_char == '=':  # assuming buffer is a list-like object and cur is the current index
			result['type'] = CPPType.CPP_MULT_EQ
		else:
			result['type'] = CPPType.CPP_MULT

	elif c == '=':
		next_char = s[1]
		if next_char == '=':
			result['type'] = CPPType.CPP_EQ_EQ
		else:
			result['type'] = CPPType.CPP_EQ

	elif c == '!':
		next_char = s[1]
		if next_char == '=':
			result['type'] = CPPType.CPP_NOT_EQ
		else:
			result['type'] = CPPType.CPP_NOT

	elif c == '^':
		next_char = s[1]
		if next_char == '=':
			result['type'] = CPPType.CPP_XOR_EQ
		else:
			result['type'] = CPPType.CPP_XOR

	elif c == '#':
		next_char = s[1]
		if next_char == '#':
			result['type'] = CPPType.CPP_PASTE
		else:
			result['type'] = CPPType.CPP_HASH
		result['val']['token_no'] = 0

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
