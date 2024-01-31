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
	CPP_NONE = 0
	CPP_WHITESPACE 	
	CPP_NEWLINE 	
	CPP_NUMBER 		
	CPP_NAME 		
	CPP_STRING_SINGLE_QUOTE
	CPP_STRING_DOUBLE_QUOTE
	CPP_MULTILINE_COMMENT 
	CPP_SINGLE_LINE_COMMENT
	CPP_DIV_EQ		
	CPP_DIV				
	CPP_LESS			
	CPP_LESS_EQ			
	CPP_SPACESHIP		
	CPP_LSHIFT_EQ		
	CPP_LSHIFT			
	CPP_OPEN_SQUARE		
	CPP_OPEN_BRACE		
	CPP_GREATER			
	CPP_GREATER_EQ		
	CPP_RSHIFT_EQ		
	CPP_RSHIFT			
	CPP_MOD				
	CPP_MOD_EQ			
	CPP_HASH			
	CPP_PASTE			
	CPP_CLOSE_BRACE		
	CPP_DOT				
	CPP_ELLIPSIS		
	CPP_DOT_STAR		
	CPP_PLUS			
	CPP_PLUS_PLUS		
	CPP_PLUS_EQ			
	CPP_MINUS			
	CPP_DEREF			
	CPP_DEREF_STAR		
	CPP_MINUS_MINUS		
	CPP_MINUS_EQ		
	CPP_AND				
	CPP_AND_AND			
	CPP_AND_EQ			
	CPP_OR				
	CPP_OR_OR			
	CPP_OR_EQ			
	CPP_COLON			
	CPP_SCOPE			
	CPP_CLOSE_SQUARE	
	CPP_MULT_EQ			
	CPP_MULT			
	CPP_EQ_EQ			
	CPP_EQ				
	CPP_NOT_EQ			
	CPP_NOT				
	CPP_XOR_EQ			
	CPP_XOR				
	CPP_QUERY			
	CPP_COMPL			
	CPP_COMMA			
	CPP_OPEN_PAREN		
	CPP_CLOSE_PAREN		
	CPP_SEMICOLON		
	CPP_OTHER			

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
	DIGRAPHS
	C_PLUS_PLUS
	SCOPE	

# RID = Reserved ID
class CPPReserved(Enum):
	# Modifiers:
	# C, in empirical order of frequency.
	RID_STATIC 		= 0
	RID_UNSIGNED 
	RID_LONG 	
	RID_CONST 	
	RID_EXTERN 	
	RID_REGISTER 
	RID_TYPEDEF 
	RID_SHORT 	
	RID_INLINE 	
	RID_VOLATILE 
	RID_SIGNED 		
	RID_AUTO 		
	RID_RESTRICT 	
	RID_NORETURN 	
	RID_ATOMIC 		

	# C extensions 
	RID_COMPLEX	
	RID_THREAD	
	RID_SAT		

	# C++
	RID_FRIEND	
	RID_VIRTUAL	
	RID_EXPLICIT
	RID_EXPORT	
	RID_MUTABLE	

	# ObjC ("PQ" reserved words - they do not appear after a '@' and are keywords only in specific contexts)
	RID_IN		
	RID_OUT		
	RID_INOUT	
	RID_BYCOPY	
	RID_BYREF	
	RID_ONEWAY	
	
	# ObjC ("PATTR" reserved words - they do not appear after a '@'  and are keywords only as property attributes)
	RID_GETTER	
	RID_SETTER	
	RID_READONLY
	RID_READWRITE
	RID_ASSIGN	
	RID_RETAIN	
	RID_COPY	
	RID_PROPATOMIC
	RID_NONATOMIC
	
	# ObjC nullability support keywords that also can appear in the
	# property attribute context.  These values should remain contiguous
	# with the other property attributes. 
	RID_NULL_UNSPECIFIED
	RID_NULLABLE		
	RID_NONNULL			
	RID_NULL_RESETTABLE	
	
	# C (reserved and imaginary types not implemented, so any use is a syntax error)
	RID_IMAGINARY		

	# C
	RID_INT		
	RID_CHAR	
	RID_FLOAT	
	RID_DOUBLE	
	RID_VOID	

	RID_ENUM	
	RID_STRUCT	
	RID_UNION	
	RID_IF		
	RID_ELSE	

	RID_WHILE	
	RID_DO		
	RID_FOR		
	RID_SWITCH	
	RID_CASE	

	RID_DEFAULT	
	RID_BREAK	
	RID_CONTINUE
	RID_RETURN	
	RID_GOTO	

	RID_SIZEOF	
	

	# C extensions
	RID_ASM			
	RID_TYPEOF	 	
	RID_TYPEOF_UNQUAL
	RID_ALIGNOF		
	RID_ATTRIBUTE	
	
	RID_VA_ARG		
	
	RID_EXTENSION	
	RID_IMAGPART	
	RID_REALPART	
	RID_LABEL		
	RID_CHOOSE_EXPR	
	
	RID_TYPES_COMPATIBLE_P
	RID_BUILTIN_COMPLEX	
	RID_BUILTIN_SHUFFLE	
	
	RID_BUILTIN_SHUFFLEVECTOR
	RID_BUILTIN_CONVERTVECTOR
	RID_BUILTIN_TGMATH		
	
	RID_BUILTIN_HAS_ATTRIBUTE
	RID_BUILTIN_ASSOC_BARRIER
	
	RID_DFLOAT32			
	RID_DFLOAT64			
	RID_DFLOAT128			
	

	# TS 18661-3 keywords, in the same sequence as the TI_* values.
	RID_FLOAT16		
	RID_FLOATN_NX_FIRST = RID_FLOAT16
	RID_FLOAT32		
	RID_FLOAT64		
	RID_FLOAT128	
	RID_FLOAT32X	
	RID_FLOAT64X	
	RID_FLOAT128X	

	RID_FRACT						
	RID_ACCUM						
	RID_AUTO_TYPE					
	RID_BUILTIN_CALL_WITH_STATIC_CHAIN
	

	# "__GIMPLE", for the GIMPLE-parsing extension to the C frontend.
	RID_GIMPLE

	# "__PHI", for parsing PHI function in GIMPLE FE.
	RID_PHI	

	# "__RTL", for the RTL-parsing extension to the C frontend.
	RID_RTL	

	# C11
	RID_ALIGNAS	
	RID_GENERIC	

	# This means to warn that this is a C++ keyword, and then treat it as a normal identifier.
	RID_CXX_COMPAT_WARN	

	# GNU transactional memory extension
	RID_TRANSACTION_ATOMIC	
	RID_TRANSACTION_RELAXED	
	RID_TRANSACTION_CANCEL	
	
	# Too many ways of getting the name of a function as a string
	RID_FUNCTION_NAME			
	RID_PRETTY_FUNCTION_NAME	
	RID_C99_FUNCTION_NAME		
	

	# C++ (some of these are keywords in Objective-C as well, but only if they appear after a '@')
	RID_BOOL
	     RID_WCHAR
	    RID_CLASS
	
	RID_PUBLIC
	   RID_PRIVATE
	  RID_PROTECTED
	
	RID_TEMPLATE
	 RID_NULL
	     RID_CATCH
	
	RID_DELETE
	   RID_FALSE
	    RID_NAMESPACE
	
	RID_NEW
	      RID_OFFSETOF
	 RID_OPERATOR
	
	RID_THIS
	     RID_THROW
	    RID_TRUE
	
	RID_TRY
	      RID_TYPENAME
	 RID_TYPEID
	
	RID_USING
	    RID_CHAR16
	   RID_CHAR32
	

	# casts
	RID_CONSTCAST
	 RID_DYNCAST
	 RID_REINTCAST
	 RID_STATCAST
	

	# C++ extensions
	RID_ADDRESSOF
	
	RID_BUILTIN_LAUNDER
	RID_BUILTIN_BIT_CAST

	# C++11
	RID_CONSTEXPR
	 RID_DECLTYPE
	 RID_NOEXCEPT
	 RID_NULLPTR
	 RID_STATIC_ASSERT
	

	# C++20
	RID_CONSTINIT
	 RID_CONSTEVAL
	

	# char8_t
	RID_CHAR8

	# C++ concepts
	RID_CONCEPT
	 RID_REQUIRES

	# C++ modules.
	RID__MODULE
	RID__IMPORT
	RID__EXPORT # Internal tokens.

	# C++ coroutines
	RID_CO_AWAIT
	 RID_CO_YIELD
	 RID_CO_RETURN

	# C++ transactional memory.
	RID_ATOMIC_NOEXCEPT
	RID_ATOMIC_CANCEL
	RID_SYNCHRONIZED

	# Objective-C ("AT" reserved words - they are only keywords when they follow '@')
	RID_AT_ENCODE,   RID_AT_END,
	RID_AT_CLASS,    RID_AT_ALIAS,     RID_AT_DEFS,
	RID_AT_PRIVATE,  RID_AT_PROTECTED, RID_AT_PUBLIC,  RID_AT_PACKAGE,
	RID_AT_PROTOCOL, RID_AT_SELECTOR,
	RID_AT_THROW,	   RID_AT_TRY,       RID_AT_CATCH,
	RID_AT_FINALLY,  RID_AT_SYNCHRONIZED, 
	RID_AT_OPTIONAL, RID_AT_REQUIRED, RID_AT_PROPERTY,
	RID_AT_SYNTHESIZE, RID_AT_DYNAMIC,
	RID_AT_INTERFACE,
	RID_AT_IMPLEMENTATION,

	# OpenMP
	RID_OMP_ALL_MEMORY,

	# Named address support, mapping the keyword to a particular named address
	# number.  Named address space 0 is reserved for the generic address.  If
	# there are more than 254 named addresses, the addr_space_t type will need
	# to be grown from an unsigned char to unsigned short.
	RID_ADDR_SPACE_0,		# generic address
	RID_ADDR_SPACE_1,
	RID_ADDR_SPACE_2,
	RID_ADDR_SPACE_3,
	RID_ADDR_SPACE_4,
	RID_ADDR_SPACE_5,
	RID_ADDR_SPACE_6,
	RID_ADDR_SPACE_7,
	RID_ADDR_SPACE_8,
	RID_ADDR_SPACE_9,
	RID_ADDR_SPACE_10,
	RID_ADDR_SPACE_11,
	RID_ADDR_SPACE_12,
	RID_ADDR_SPACE_13,
	RID_ADDR_SPACE_14,
	RID_ADDR_SPACE_15,

	RID_FIRST_ADDR_SPACE = RID_ADDR_SPACE_0,
	RID_LAST_ADDR_SPACE = RID_ADDR_SPACE_15,

	# __intN keywords.  The _N_M here doesn't correspond to the intN
	# in the keyword; use the bitsize in int_n_t_data_t[M] for that.
	# For example, if int_n_t_data_t[0].bitsize is 13, then RID_INT_N_0
	# is for __int13.

	# Note that the range to use is RID_FIRST_INT_N through
	# RID_FIRST_INT_N + NUM_INT_N_ENTS - 1 and c-parser.cc has a list of
	# all RID_INT_N_* in a case statement.

	RID_INT_N_0,
	RID_INT_N_1,
	RID_INT_N_2,
	RID_INT_N_3,

	RID_FIRST_INT_N = RID_INT_N_0,
	RID_LAST_INT_N = RID_INT_N_3,

	RID_MAX,

	RID_FIRST_MODIFIER = RID_STATIC,
	RID_LAST_MODIFIER = RID_ONEWAY,

	RID_FIRST_CXX11 = RID_CONSTEXPR,
	RID_LAST_CXX11 = RID_STATIC_ASSERT,
	RID_FIRST_CXX20 = RID_CONSTINIT,
	RID_LAST_CXX20 = RID_CO_RETURN,
	RID_FIRST_AT = RID_AT_ENCODE,
	RID_LAST_AT = RID_AT_IMPLEMENTATION,
	RID_FIRST_PQ = RID_IN,
	RID_LAST_PQ = RID_ONEWAY,
	RID_FIRST_PATTR = RID_GETTER,
	RID_LAST_PATTR = RID_NULL_RESETTABLE


const struct c_common_resword c_common_reswords[] =
{
	{ "_Alignas",		RID_ALIGNAS,   D_CONLY },
	{ "_Alignof",		RID_ALIGNOF,   D_CONLY },
	{ "_Atomic",		RID_ATOMIC,    D_CONLY },
	{ "_Bool",			RID_BOOL,      D_CONLY },
	{ "_Complex",		RID_COMPLEX,	0 },
	{ "_Imaginary",		RID_IMAGINARY, D_CONLY },
	{ "_Float16",         RID_FLOAT16,    0 },
	{ "_Float32",         RID_FLOAT32,    0 },
	{ "_Float64",         RID_FLOAT64,    0 },
	{ "_Float128",        RID_FLOAT128,   0 },
	{ "_Float32x",        RID_FLOAT32X,   0 },
	{ "_Float64x",        RID_FLOAT64X,   0 },
	{ "_Float128x",       RID_FLOAT128X,  0 },
	{ "_Decimal32",       RID_DFLOAT32,  D_CONLY },
	{ "_Decimal64",       RID_DFLOAT64,  D_CONLY },
	{ "_Decimal128",      RID_DFLOAT128, D_CONLY },
	{ "_Fract",           RID_FRACT,     D_CONLY | D_EXT },
	{ "_Accum",           RID_ACCUM,     D_CONLY | D_EXT },
	{ "_Sat",             RID_SAT,       D_CONLY | D_EXT },
	{ "_Static_assert",   RID_STATIC_ASSERT, D_CONLY },
	{ "_Noreturn",        RID_NORETURN,  D_CONLY },
	{ "_Generic",         RID_GENERIC,   D_CONLY },
	{ "_Thread_local",    RID_THREAD,    D_CONLY },
	{ "__FUNCTION__",	RID_FUNCTION_NAME, 0 },
	{ "__PRETTY_FUNCTION__", RID_PRETTY_FUNCTION_NAME, 0 },
	{ "__alignof",	RID_ALIGNOF,	0 },
	{ "__alignof__",	RID_ALIGNOF,	0 },
	{ "__asm",		RID_ASM,	0 },
	{ "__asm__",		RID_ASM,	0 },
	{ "__attribute",	RID_ATTRIBUTE,	0 },
	{ "__attribute__",	RID_ATTRIBUTE,	0 },
	{ "__auto_type",	RID_AUTO_TYPE,	D_CONLY },
	{ "__builtin_addressof", RID_ADDRESSOF, D_CXXONLY },
	{ "__builtin_bit_cast", RID_BUILTIN_BIT_CAST, D_CXXONLY },
	{ "__builtin_call_with_static_chain",
		RID_BUILTIN_CALL_WITH_STATIC_CHAIN, D_CONLY },
	{ "__builtin_choose_expr", RID_CHOOSE_EXPR, D_CONLY },
	{ "__builtin_complex", RID_BUILTIN_COMPLEX, D_CONLY },
	{ "__builtin_convertvector", RID_BUILTIN_CONVERTVECTOR, 0 },
	{ "__builtin_has_attribute", RID_BUILTIN_HAS_ATTRIBUTE, 0 },
	{ "__builtin_launder", RID_BUILTIN_LAUNDER, D_CXXONLY },
	{ "__builtin_assoc_barrier", RID_BUILTIN_ASSOC_BARRIER, 0 },
	{ "__builtin_shuffle", RID_BUILTIN_SHUFFLE, 0 },
	{ "__builtin_shufflevector", RID_BUILTIN_SHUFFLEVECTOR, 0 },
	{ "__builtin_tgmath", RID_BUILTIN_TGMATH, D_CONLY },
	{ "__builtin_offsetof", RID_OFFSETOF, 0 },
	{ "__builtin_types_compatible_p", RID_TYPES_COMPATIBLE_P, D_CONLY },
	{ "__builtin_va_arg",	RID_VA_ARG,	0 },
	{ "__complex",	RID_COMPLEX,	0 },
	{ "__complex__",	RID_COMPLEX,	0 },
	{ "__const",		RID_CONST,	0 },
	{ "__const__",	RID_CONST,	0 },
	{ "__constinit",	RID_CONSTINIT,	D_CXXONLY },
	{ "__decltype",       RID_DECLTYPE,   D_CXXONLY },
	{ "__extension__",	RID_EXTENSION,	0 },
	{ "__func__",		RID_C99_FUNCTION_NAME, 0 },
	{ "__imag",		RID_IMAGPART,	0 },
	{ "__imag__",		RID_IMAGPART,	0 },
	{ "__inline",		RID_INLINE,	0 },
	{ "__inline__",	RID_INLINE,	0 },
	{ "__label__",	RID_LABEL,	0 },
	{ "__null",		RID_NULL,	0 },
	{ "__real",		RID_REALPART,	0 },
	{ "__real__",		RID_REALPART,	0 },
	{ "__restrict",	RID_RESTRICT,	0 },
	{ "__restrict__",	RID_RESTRICT,	0 },
	{ "__signed",		RID_SIGNED,	0 },
	{ "__signed__",	RID_SIGNED,	0 },
	{ "__thread",		RID_THREAD,	0 },
	{ "__transaction_atomic", RID_TRANSACTION_ATOMIC, 0 },
	{ "__transaction_relaxed", RID_TRANSACTION_RELAXED, 0 },
	{ "__transaction_cancel", RID_TRANSACTION_CANCEL, 0 },
	{ "__typeof",		RID_TYPEOF,	0 },
	{ "__typeof__",	RID_TYPEOF,	0 },
	{ "__volatile",	RID_VOLATILE,	0 },
	{ "__volatile__",	RID_VOLATILE,	0 },
	{ "__GIMPLE",		RID_GIMPLE,	D_CONLY },
	{ "__PHI",		RID_PHI,	D_CONLY },
	{ "__RTL",		RID_RTL,	D_CONLY },
	{ "alignas",		RID_ALIGNAS,	D_C2X | D_CXX11 | D_CXXWARN },
	{ "alignof",		RID_ALIGNOF,	D_C2X | D_CXX11 | D_CXXWARN },
	{ "asm",		RID_ASM,	D_ASM },
	{ "auto",		RID_AUTO,	0 },
	{ "bool",		RID_BOOL,	D_C2X | D_CXXWARN },
	{ "break",		RID_BREAK,	0 },
	{ "case",		RID_CASE,	0 },
	{ "catch",		RID_CATCH,	D_CXX_OBJC | D_CXXWARN },
	{ "char",		RID_CHAR,	0 },
	{ "char8_t",		RID_CHAR8,	D_CXX_CHAR8_T_FLAGS | D_CXXWARN },
	{ "char16_t",		RID_CHAR16,	D_CXXONLY | D_CXX11 | D_CXXWARN },
	{ "char32_t",		RID_CHAR32,	D_CXXONLY | D_CXX11 | D_CXXWARN },
	{ "class",		RID_CLASS,	D_CXX_OBJC | D_CXXWARN },
	{ "const",		RID_CONST,	0 },
	{ "consteval",	RID_CONSTEVAL,	D_CXXONLY | D_CXX20 | D_CXXWARN },
	{ "constexpr",	RID_CONSTEXPR,	D_C2X | D_CXX11 | D_CXXWARN },
	{ "constinit",	RID_CONSTINIT,	D_CXXONLY | D_CXX20 | D_CXXWARN },
	{ "const_cast",	RID_CONSTCAST,	D_CXXONLY | D_CXXWARN },
	{ "continue",		RID_CONTINUE,	0 },
	{ "decltype",         RID_DECLTYPE,   D_CXXONLY | D_CXX11 | D_CXXWARN },
	{ "default",		RID_DEFAULT,	0 },
	{ "delete",		RID_DELETE,	D_CXXONLY | D_CXXWARN },
	{ "do",		RID_DO,		0 },
	{ "double",		RID_DOUBLE,	0 },
	{ "dynamic_cast",	RID_DYNCAST,	D_CXXONLY | D_CXXWARN },
	{ "else",		RID_ELSE,	0 },
	{ "enum",		RID_ENUM,	0 },
	{ "explicit",		RID_EXPLICIT,	D_CXXONLY | D_CXXWARN },
	{ "export",		RID_EXPORT,	D_CXXONLY | D_CXXWARN },
	{ "extern",		RID_EXTERN,	0 },
	{ "false",		RID_FALSE,	D_C2X | D_CXXWARN },
	{ "float",		RID_FLOAT,	0 },
	{ "for",		RID_FOR,	0 },
	{ "friend",		RID_FRIEND,	D_CXXONLY | D_CXXWARN },
	{ "goto",		RID_GOTO,	0 },
	{ "if",		RID_IF,		0 },
	{ "inline",		RID_INLINE,	D_EXT89 },
	{ "int",		RID_INT,	0 },
	{ "long",		RID_LONG,	0 },
	{ "mutable",		RID_MUTABLE,	D_CXXONLY | D_CXXWARN },
	{ "namespace",	RID_NAMESPACE,	D_CXXONLY | D_CXXWARN },
	{ "new",		RID_NEW,	D_CXXONLY | D_CXXWARN },
	{ "noexcept",		RID_NOEXCEPT,	D_CXXONLY | D_CXX11 | D_CXXWARN },
	{ "nullptr",		RID_NULLPTR,	D_C2X | D_CXX11 | D_CXXWARN },
	{ "operator",		RID_OPERATOR,	D_CXXONLY | D_CXXWARN },
	{ "private",		RID_PRIVATE,	D_CXX_OBJC | D_CXXWARN },
	{ "protected",	RID_PROTECTED,	D_CXX_OBJC | D_CXXWARN },
	{ "public",		RID_PUBLIC,	D_CXX_OBJC | D_CXXWARN },
	{ "register",		RID_REGISTER,	0 },
	{ "reinterpret_cast",	RID_REINTCAST,	D_CXXONLY | D_CXXWARN },
	{ "restrict",		RID_RESTRICT,	D_CONLY | D_C99 },
	{ "return",		RID_RETURN,	0 },
	{ "short",		RID_SHORT,	0 },
	{ "signed",		RID_SIGNED,	0 },
	{ "sizeof",		RID_SIZEOF,	0 },
	{ "static",		RID_STATIC,	0 },
	{ "static_assert",    RID_STATIC_ASSERT, D_C2X | D_CXX11 | D_CXXWARN },
	{ "static_cast",	RID_STATCAST,	D_CXXONLY | D_CXXWARN },
	{ "struct",		RID_STRUCT,	0 },
	{ "switch",		RID_SWITCH,	0 },
	{ "template",		RID_TEMPLATE,	D_CXXONLY | D_CXXWARN },
	{ "this",		RID_THIS,	D_CXXONLY | D_CXXWARN },
	{ "thread_local",	RID_THREAD,	D_C2X | D_CXX11 | D_CXXWARN },
	{ "throw",		RID_THROW,	D_CXX_OBJC | D_CXXWARN },
	{ "true",		RID_TRUE,	D_C2X | D_CXXWARN },
	{ "try",		RID_TRY,	D_CXX_OBJC | D_CXXWARN },
	{ "typedef",		RID_TYPEDEF,	0 },
	{ "typename",		RID_TYPENAME,	D_CXXONLY | D_CXXWARN },
	{ "typeid",		RID_TYPEID,	D_CXXONLY | D_CXXWARN },
	{ "typeof",		RID_TYPEOF,	D_EXT11 },
	{ "typeof_unqual",	RID_TYPEOF_UNQUAL,	D_CONLY | D_C2X },
	{ "union",		RID_UNION,	0 },
	{ "unsigned",		RID_UNSIGNED,	0 },
	{ "using",		RID_USING,	D_CXXONLY | D_CXXWARN },
	{ "virtual",		RID_VIRTUAL,	D_CXXONLY | D_CXXWARN },
	{ "void",		RID_VOID,	0 },
	{ "volatile",		RID_VOLATILE,	0 },
	{ "wchar_t",		RID_WCHAR,	D_CXXONLY },
	{ "while",		RID_WHILE,	0 },
}

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