# Prerequisite
# pip install pathlib

import include
import glob
import os
import sys
from pathlib import Path
import re
import subprocess
import enum

# input in temrinal:
# run command:
# 'python allFileMakefile.py repo'
# then when u put this code 'print(len(sys.argv))'
# will output 2

# this means, only run this if this file is directly called from terminal
# not from imported module
if __name__ == "__main__":
	if (len(sys.argv) < 2):
		print("Wrong argument. Terminating script.")
		sys.exit()

	dir_list = []
	dir_list.append(sys.argv[1])


class CPPType(enum.Enum):
	CPP_NONE = 0
	CPP_WHITESPACE = enum.auto()
	CPP_NEWLINE = enum.auto()
	CPP_NUMBER = enum.auto()
	CPP_NAME = enum.auto()
	CPP_STRING_SINGLE_QUOTE = enum.auto()
	CPP_STRING_DOUBLE_QUOTE = enum.auto()
	CPP_MULTILINE_COMMENT = enum.auto()
	CPP_SINGLE_LINE_COMMENT = enum.auto()
	CPP_DIV_EQ = enum.auto()
	CPP_DIV = enum.auto()
	CPP_LESS = enum.auto()
	CPP_LESS_EQ = enum.auto()
	CPP_SPACESHIP = enum.auto()
	CPP_LSHIFT_EQ = enum.auto()
	CPP_LSHIFT = enum.auto()
	CPP_OPEN_SQUARE = enum.auto()
	CPP_OPEN_BRACE = enum.auto()
	CPP_GREATER = enum.auto()
	CPP_GREATER_EQ = enum.auto()
	CPP_RSHIFT_EQ = enum.auto()
	CPP_RSHIFT = enum.auto()
	CPP_MOD = enum.auto()
	CPP_MOD_EQ = enum.auto()
	CPP_HASH = enum.auto()
	CPP_PASTE = enum.auto()
	CPP_CLOSE_BRACE = enum.auto()
	CPP_DOT = enum.auto()
	CPP_ELLIPSIS = enum.auto()
	CPP_DOT_STAR = enum.auto()
	CPP_PLUS = enum.auto()
	CPP_PLUS_PLUS = enum.auto()
	CPP_PLUS_EQ = enum.auto()
	CPP_MINUS = enum.auto()
	CPP_DEREF = enum.auto()
	CPP_DEREF_STAR = enum.auto()
	CPP_MINUS_MINUS = enum.auto()
	CPP_MINUS_EQ = enum.auto()
	CPP_AND = enum.auto()
	CPP_AND_AND = enum.auto()
	CPP_AND_EQ = enum.auto()
	CPP_OR = enum.auto()
	CPP_OR_OR = enum.auto()
	CPP_OR_EQ = enum.auto()
	CPP_COLON = enum.auto()
	CPP_SCOPE = enum.auto()
	CPP_CLOSE_SQUARE = enum.auto()
	CPP_MULT_EQ = enum.auto()
	CPP_MULT = enum.auto()
	CPP_EQ_EQ = enum.auto()
	CPP_EQ = enum.auto()
	CPP_NOT_EQ = enum.auto()
	CPP_NOT = enum.auto()
	CPP_XOR_EQ = enum.auto()
	CPP_XOR = enum.auto()
	CPP_QUERY = enum.auto()
	CPP_COMPL = enum.auto()
	CPP_COMMA = enum.auto()
	CPP_OPEN_PAREN = enum.auto()
	CPP_CLOSE_PAREN = enum.auto()
	CPP_SEMICOLON = enum.auto()
	CPP_OTHER = enum.auto()

	# Below here is i self add one
	CPP_PARENTHESIS = enum.auto()
	CPP_BRACE = enum.auto()


class CPP_Flag(enum.Enum):
	"""
	flags should be bit-wised
	1 = 0001
	2 = 0010
	4 = 0100
	8 = 1000
	and so on
	"""
	NONE = 1
	DIGRAPH = 2


class CPPOption(enum.Enum):
	NONE = 0
	DIGRAPHS = enum.auto()
	C_PLUS_PLUS = enum.auto()
	SCOPE = enum.auto()

# RID = Reserved ID


class CPPReserved(enum.Enum):
	# Modifiers:
	# C, in empirical order of frequency.
	RID_STATIC = 0
	RID_UNSIGNED = enum.auto()
	RID_LONG = enum.auto()
	RID_CONST = enum.auto()
	RID_EXTERN = enum.auto()
	RID_REGISTER = enum.auto()
	RID_TYPEDEF = enum.auto()
	RID_SHORT = enum.auto()
	RID_INLINE = enum.auto()
	RID_VOLATILE = enum.auto()
	RID_SIGNED = enum.auto()
	RID_AUTO = enum.auto()
	RID_RESTRICT = enum.auto()
	RID_NORETURN = enum.auto()
	RID_ATOMIC = enum.auto()

	# C extensions
	RID_COMPLEX = enum.auto()
	RID_THREAD = enum.auto()
	RID_SAT = enum.auto()

	# C++
	RID_FRIEND = enum.auto()
	RID_VIRTUAL = enum.auto()
	RID_EXPLICIT = enum.auto()
	RID_EXPORT = enum.auto()
	RID_MUTABLE = enum.auto()

	# ObjC ("PQ" reserved words - they do not appear after a '@' and are keywords only in specific contexts)
	RID_IN = enum.auto()
	RID_OUT = enum.auto()
	RID_INOUT = enum.auto()
	RID_BYCOPY = enum.auto()
	RID_BYREF = enum.auto()
	RID_ONEWAY = enum.auto()

	# ObjC ("PATTR" reserved words - they do not appear after a '@'  and are keywords only as property attributes)
	RID_GETTER = enum.auto()
	RID_SETTER = enum.auto()
	RID_READONLY = enum.auto()
	RID_READWRITE = enum.auto()
	RID_ASSIGN = enum.auto()
	RID_RETAIN = enum.auto()
	RID_COPY = enum.auto()
	RID_PROPATOMIC = enum.auto()
	RID_NONATOMIC = enum.auto()

	# ObjC nullability support keywords that also can appear in the
	# property attribute context.  These values should remain contiguous
	# with the other property attributes.
	RID_NULL_UNSPECIFIED = enum.auto()
	RID_NULLABLE = enum.auto()
	RID_NONNULL = enum.auto()
	RID_NULL_RESETTABLE = enum.auto()

	# C (reserved and imaginary types not implemented, so any use is a syntax error)
	RID_IMAGINARY = enum.auto()

	# C
	RID_INT = enum.auto()
	RID_CHAR = enum.auto()
	RID_FLOAT = enum.auto()
	RID_DOUBLE = enum.auto()
	RID_VOID = enum.auto()

	RID_ENUM = enum.auto()
	RID_STRUCT = enum.auto()
	RID_UNION = enum.auto()
	RID_IF = enum.auto()
	RID_ELSE = enum.auto()

	RID_WHILE = enum.auto()
	RID_DO = enum.auto()
	RID_FOR = enum.auto()
	RID_SWITCH = enum.auto()
	RID_CASE = enum.auto()

	RID_DEFAULT = enum.auto()
	RID_BREAK = enum.auto()
	RID_CONTINUE = enum.auto()
	RID_RETURN = enum.auto()
	RID_GOTO = enum.auto()

	RID_SIZEOF = enum.auto()

	# C extensions
	RID_ASM = enum.auto()
	RID_TYPEOF = enum.auto()
	RID_TYPEOF_UNQUAL = enum.auto()
	RID_ALIGNOF = enum.auto()
	RID_ATTRIBUTE = enum.auto()

	RID_VA_ARG = enum.auto()

	RID_EXTENSION = enum.auto()
	RID_IMAGPART = enum.auto()
	RID_REALPART = enum.auto()
	RID_LABEL = enum.auto()
	RID_CHOOSE_EXPR = enum.auto()

	RID_TYPES_COMPATIBLE_P = enum.auto()
	RID_BUILTIN_COMPLEX = enum.auto()
	RID_BUILTIN_SHUFFLE = enum.auto()

	RID_BUILTIN_SHUFFLEVECTOR = enum.auto()
	RID_BUILTIN_CONVERTVECTOR = enum.auto()
	RID_BUILTIN_TGMATH = enum.auto()

	RID_BUILTIN_HAS_ATTRIBUTE = enum.auto()
	RID_BUILTIN_ASSOC_BARRIER = enum.auto()

	RID_DFLOAT32 = enum.auto()
	RID_DFLOAT64 = enum.auto()
	RID_DFLOAT128 = enum.auto()

	# TS 18661-3 keywords, in the same sequence as the TI_* values.
	RID_FLOAT16 = enum.auto()
	RID_FLOATN_NX_FIRST = RID_FLOAT16
	RID_FLOAT32 = enum.auto()
	RID_FLOAT64 = enum.auto()
	RID_FLOAT128 = enum.auto()
	RID_FLOAT32X = enum.auto()
	RID_FLOAT64X = enum.auto()
	RID_FLOAT128X = enum.auto()

	RID_FRACT = enum.auto()
	RID_ACCUM = enum.auto()
	RID_AUTO_TYPE = enum.auto()
	RID_BUILTIN_CALL_WITH_STATIC_CHAIN = enum.auto()

	# "__GIMPLE", for the GIMPLE-parsing extension to the C frontend.
	RID_GIMPLE = enum.auto()

	# "__PHI", for parsing PHI function in GIMPLE FE.
	RID_PHI = enum.auto()

	# "__RTL", for the RTL-parsing extension to the C frontend.
	RID_RTL = enum.auto()

	# C11
	RID_ALIGNAS = enum.auto()
	RID_GENERIC = enum.auto()

	# This means to warn that this is a C++ keyword, and then treat it as a normal identifier.
	RID_CXX_COMPAT_WARN = enum.auto()

	# GNU transactional memory extension
	RID_TRANSACTION_ATOMIC = enum.auto()
	RID_TRANSACTION_RELAXED = enum.auto()
	RID_TRANSACTION_CANCEL = enum.auto()

	# Too many ways of getting the name of a function as a string
	RID_FUNCTION_NAME = enum.auto()
	RID_PRETTY_FUNCTION_NAME = enum.auto()
	RID_C99_FUNCTION_NAME = enum.auto()

	# C++ (some of these are keywords in Objective-C as well, but only if they appear after a '@')
	RID_BOOL = enum.auto()
	RID_WCHAR = enum.auto()
	RID_CLASS = enum.auto()

	RID_PUBLIC = enum.auto()
	RID_PRIVATE = enum.auto()
	RID_PROTECTED = enum.auto()

	RID_TEMPLATE = enum.auto()
	RID_NULL = enum.auto()
	RID_CATCH = enum.auto()

	RID_DELETE = enum.auto()
	RID_FALSE = enum.auto()
	RID_NAMESPACE = enum.auto()

	RID_NEW = enum.auto()
	RID_OFFSETOF = enum.auto()
	RID_OPERATOR = enum.auto()

	RID_THIS = enum.auto()
	RID_THROW = enum.auto()
	RID_TRUE = enum.auto()

	RID_TRY = enum.auto()
	RID_TYPENAME = enum.auto()
	RID_TYPEID = enum.auto()

	RID_USING = enum.auto()
	RID_CHAR16 = enum.auto()
	RID_CHAR32 = enum.auto()

	# casts
	RID_CONSTCAST = enum.auto()
	RID_DYNCAST = enum.auto()
	RID_REINTCAST = enum.auto()
	RID_STATCAST = enum.auto()

	# C++ extensions
	RID_ADDRESSOF = enum.auto()

	RID_BUILTIN_LAUNDER = enum.auto()
	RID_BUILTIN_BIT_CAST = enum.auto()

	# C++11
	RID_CONSTEXPR = enum.auto()
	RID_DECLTYPE = enum.auto()
	RID_NOEXCEPT = enum.auto()
	RID_NULLPTR = enum.auto()
	RID_STATIC_ASSERT = enum.auto()

	# C++20
	RID_CONSTINIT = enum.auto()
	RID_CONSTEVAL = enum.auto()

	# char8_t
	RID_CHAR8 = enum.auto()

	# C++ concepts
	RID_CONCEPT = enum.auto()
	RID_REQUIRES = enum.auto()

	# C++ modules.
	RID__MODULE = enum.auto()
	RID__IMPORT = enum.auto()
	RID__EXPORT = enum.auto()  # Internal tokens.

	# C++ coroutines
	RID_CO_AWAIT = enum.auto()
	RID_CO_YIELD = enum.auto()
	RID_CO_RETURN = enum.auto()

	# C++ transactional memory.
	RID_ATOMIC_NOEXCEPT = enum.auto()
	RID_ATOMIC_CANCEL = enum.auto()
	RID_SYNCHRONIZED = enum.auto()

	# Objective-C ("AT" reserved words - they are only keywords when they follow '@')
	RID_AT_ENCODE = enum.auto()
	RID_AT_END = enum.auto()

	RID_AT_CLASS = enum.auto()
	RID_AT_ALIAS = enum.auto()
	RID_AT_DEFS = enum.auto()

	RID_AT_PRIVATE = enum.auto()
	RID_AT_PROTECTED = enum.auto()
	RID_AT_PUBLIC = enum.auto()
	RID_AT_PACKAGE = enum.auto()

	RID_AT_PROTOCOL = enum.auto()
	RID_AT_SELECTOR = enum.auto()

	RID_AT_THROW = enum.auto()
	RID_AT_TRY = enum.auto()
	RID_AT_CATCH = enum.auto()

	RID_AT_FINALLY = enum.auto()
	RID_AT_SYNCHRONIZED = enum.auto()

	RID_AT_OPTIONAL = enum.auto()
	RID_AT_REQUIRED = enum.auto()
	RID_AT_PROPERTY = enum.auto()

	RID_AT_SYNTHESIZE = enum.auto()
	RID_AT_DYNAMIC = enum.auto()

	RID_AT_INTERFACE = enum.auto()

	RID_AT_IMPLEMENTATION = enum.auto()


	# OpenMP
	RID_OMP_ALL_MEMORY = enum.auto()

	# Named address support, mapping the keyword to a particular named address
	# number.  Named address space 0 is reserved for the generic address.  If
	# there are more than 254 named addresses, the addr_space_t type will need
	# to be grown from an unsigned char to unsigned short.
	RID_ADDR_SPACE_0 = enum.auto()		# generic address
	RID_ADDR_SPACE_1 = enum.auto()
	RID_ADDR_SPACE_2 = enum.auto()
	RID_ADDR_SPACE_3 = enum.auto()
	RID_ADDR_SPACE_4 = enum.auto()
	RID_ADDR_SPACE_5 = enum.auto()
	RID_ADDR_SPACE_6 = enum.auto()
	RID_ADDR_SPACE_7 = enum.auto()
	RID_ADDR_SPACE_8 = enum.auto()
	RID_ADDR_SPACE_9 = enum.auto()
	RID_ADDR_SPACE_10 = enum.auto()
	RID_ADDR_SPACE_11 = enum.auto()
	RID_ADDR_SPACE_12 = enum.auto()
	RID_ADDR_SPACE_13 = enum.auto()
	RID_ADDR_SPACE_14 = enum.auto()
	RID_ADDR_SPACE_15 = enum.auto()

	RID_FIRST_ADDR_SPACE = RID_ADDR_SPACE_0
	RID_LAST_ADDR_SPACE = RID_ADDR_SPACE_15

	# __intN keywords.  The _N_M here doesn't correspond to the intN
	# in the keyword; use the bitsize in int_n_t_data_t[M] for that.
	# For example, if int_n_t_data_t[0].bitsize is 13, then RID_INT_N_0
	# is for __int13.

	# Note that the range to use is RID_FIRST_INT_N through
	# RID_FIRST_INT_N + NUM_INT_N_ENTS - 1 and c-parser.cc has a list of
	# all RID_INT_N_* in a case statement.

	RID_INT_N_0 = enum.auto()
	RID_INT_N_1 = enum.auto()
	RID_INT_N_2 = enum.auto()
	RID_INT_N_3 = enum.auto()

	RID_FIRST_INT_N = RID_INT_N_0
	RID_LAST_INT_N = RID_INT_N_3

	RID_MAX = enum.auto()

	RID_FIRST_MODIFIER = RID_STATIC
	RID_LAST_MODIFIER = RID_ONEWAY

	RID_FIRST_CXX11 = RID_CONSTEXPR
	RID_LAST_CXX11 = RID_STATIC_ASSERT
	RID_FIRST_CXX20 = RID_CONSTINIT
	RID_LAST_CXX20 = RID_CO_RETURN
	RID_FIRST_AT = RID_AT_ENCODE
	RID_LAST_AT = RID_AT_IMPLEMENTATION
	RID_FIRST_PQ = RID_IN
	RID_LAST_PQ = RID_ONEWAY
	RID_FIRST_PATTR = RID_GETTER
	RID_LAST_PATTR = RID_NULL_RESETTABLE

# The last element is 'disable' in original code
# But i just change to 0 for the moment, i dk got what use
c_reserved_words = [
	{ "_Alignas",			CPPReserved.RID_ALIGNAS,   0 },
	{ "_Alignof",			CPPReserved.RID_ALIGNOF,   0 },
	{ "_Atomic",			CPPReserved.RID_ATOMIC,    0 },
	{ "_Bool",				CPPReserved.RID_BOOL,      0 },
	{ "_Complex",			CPPReserved.RID_COMPLEX,	0 },
	{ "_Imaginary",			CPPReserved.RID_IMAGINARY, 0 },
	{ "_Float16",         	CPPReserved.RID_FLOAT16,    0 },
	{ "_Float32",         	CPPReserved.RID_FLOAT32,    0 },
	{ "_Float64",         	CPPReserved.RID_FLOAT64,    0 },
	{ "_Float128",        	CPPReserved.RID_FLOAT128,   0 },
	{ "_Float32x",        	CPPReserved.RID_FLOAT32X,   0 },
	{ "_Float64x",        	CPPReserved.RID_FLOAT64X,   0 },
	{ "_Float128x",       	CPPReserved.RID_FLOAT128X,  0 },
	{ "_Decimal32",       	CPPReserved.RID_DFLOAT32,  0 },
	{ "_Decimal64",       	CPPReserved.RID_DFLOAT64,  0 },
	{ "_Decimal128",      	CPPReserved.RID_DFLOAT128, 0 },
	{ "_Fract",           	CPPReserved.RID_FRACT,     0 },
	{ "_Accum",           	CPPReserved.RID_ACCUM,     0 },
	{ "_Sat",             	CPPReserved.RID_SAT,       0 },
	{ "_Static_assert",   	CPPReserved.RID_STATIC_ASSERT, 0 },
	{ "_Noreturn",        	CPPReserved.RID_NORETURN,  0 },
	{ "_Generic",         	CPPReserved.RID_GENERIC,   0 },
	{ "_Thread_local",    	CPPReserved.RID_THREAD,    0 },
	{ "__FUNCTION__",		CPPReserved.RID_FUNCTION_NAME, 0 },
	{ "__PRETTY_FUNCTION__", 	CPPReserved.RID_PRETTY_FUNCTION_NAME, 0 },
	{ "__alignof",			CPPReserved.RID_ALIGNOF,	0 },
	{ "__alignof__",		CPPReserved.RID_ALIGNOF,	0 },
	{ "__asm",				CPPReserved.RID_ASM,	0 },
	{ "__asm__",			CPPReserved.RID_ASM,	0 },
	{ "__attribute",		CPPReserved.RID_ATTRIBUTE,	0 },
	{ "__attribute__",		CPPReserved.RID_ATTRIBUTE,	0 },
	{ "__auto_type",		CPPReserved.RID_AUTO_TYPE,	0 },
	{ "__builtin_addressof", 	CPPReserved.RID_ADDRESSOF, 0 },
	{ "__builtin_bit_cast", 	CPPReserved.RID_BUILTIN_BIT_CAST, 0 },
	{ "__builtin_call_with_static_chain",	CPPReserved.RID_BUILTIN_CALL_WITH_STATIC_CHAIN, 0 },
	{ "__builtin_choose_expr", 		CPPReserved.RID_CHOOSE_EXPR, 0 },
	{ "__builtin_complex", 			CPPReserved.RID_BUILTIN_COMPLEX, 0 },
	{ "__builtin_convertvector",	CPPReserved.RID_BUILTIN_CONVERTVECTOR, 0 },
	{ "__builtin_has_attribute", 	CPPReserved.RID_BUILTIN_HAS_ATTRIBUTE, 0 },
	{ "__builtin_launder", 			CPPReserved.RID_BUILTIN_LAUNDER, 0 },
	{ "__builtin_assoc_barrier", 	CPPReserved.RID_BUILTIN_ASSOC_BARRIER, 0 },
	{ "__builtin_shuffle", 			CPPReserved.RID_BUILTIN_SHUFFLE, 0 },
	{ "__builtin_shufflevector", 	CPPReserved.RID_BUILTIN_SHUFFLEVECTOR, 0 },
	{ "__builtin_tgmath", 			CPPReserved.RID_BUILTIN_TGMATH, 0 },
	{ "__builtin_offsetof", 		CPPReserved.RID_OFFSETOF, 0 },
	{ "__builtin_types_compatible_p", 	CPPReserved.RID_TYPES_COMPATIBLE_P, 0 },
	{ "__builtin_va_arg",	CPPReserved.RID_VA_ARG,	0 },
	{ "__complex",			CPPReserved.RID_COMPLEX,	0 },
	{ "__complex__",		CPPReserved.RID_COMPLEX,	0 },
	{ "__const",			CPPReserved.RID_CONST,	0 },
	{ "__const__",			CPPReserved.RID_CONST,	0 },
	{ "__constinit",		CPPReserved.RID_CONSTINIT,	0 },
	{ "__decltype",       	CPPReserved.RID_DECLTYPE,   0 },
	{ "__extension__",		CPPReserved.RID_EXTENSION,	0 },
	{ "__func__",			CPPReserved.RID_C99_FUNCTION_NAME, 0 },
	{ "__imag",				CPPReserved.RID_IMAGPART,	0 },
	{ "__imag__",			CPPReserved.RID_IMAGPART,	0 },
	{ "__inline",			CPPReserved.RID_INLINE,	0 },
	{ "__inline__",			CPPReserved.RID_INLINE,	0 },
	{ "__label__",			CPPReserved.RID_LABEL,	0 },
	{ "__null",				CPPReserved.RID_NULL,	0 },
	{ "__real",				CPPReserved.RID_REALPART,	0 },
	{ "__real__",			CPPReserved.RID_REALPART,	0 },
	{ "__restrict",			CPPReserved.RID_RESTRICT,	0 },
	{ "__restrict__",		CPPReserved.RID_RESTRICT,	0 },
	{ "__signed",			CPPReserved.RID_SIGNED,	0 },
	{ "__signed__",			CPPReserved.RID_SIGNED,	0 },
	{ "__thread",			CPPReserved.RID_THREAD,	0 },
	{ "__transaction_atomic", 	CPPReserved.RID_TRANSACTION_ATOMIC, 0 },
	{ "__transaction_relaxed", 	CPPReserved.RID_TRANSACTION_RELAXED, 0 },
	{ "__transaction_cancel", 	CPPReserved.RID_TRANSACTION_CANCEL, 0 },
	{ "__typeof",		CPPReserved.RID_TYPEOF,	0 },
	{ "__typeof__",		CPPReserved.RID_TYPEOF,	0 },
	{ "__volatile",		CPPReserved.RID_VOLATILE,	0 },
	{ "__volatile__",	CPPReserved.RID_VOLATILE,	0 },
	{ "__GIMPLE",		CPPReserved.RID_GIMPLE,	0 },
	{ "__PHI",			CPPReserved.RID_PHI,	0 },
	{ "__RTL",			CPPReserved.RID_RTL,	0 },
	{ "alignas",		CPPReserved.RID_ALIGNAS,	0 },
	{ "alignof",		CPPReserved.RID_ALIGNOF,	0 },
	{ "asm",			CPPReserved.RID_ASM,	0 },
	{ "auto",			CPPReserved.RID_AUTO,	0 },
	{ "bool",			CPPReserved.RID_BOOL,	0 },
	{ "break",			CPPReserved.RID_BREAK,	0 },
	{ "case",			CPPReserved.RID_CASE,	0 },
	{ "catch",			CPPReserved.RID_CATCH,	0 },
	{ "char",			CPPReserved.RID_CHAR,	0 },
	{ "char8_t",		CPPReserved.RID_CHAR8,	0 },
	{ "char16_t",		CPPReserved.RID_CHAR16,	0 },
	{ "char32_t",		CPPReserved.RID_CHAR32,	0 },
	{ "class",			CPPReserved.RID_CLASS,	0 },
	{ "const",			CPPReserved.RID_CONST,	0 },
	{ "consteval",		CPPReserved.RID_CONSTEVAL,	0 },
	{ "constexpr",		CPPReserved.RID_CONSTEXPR,	0 },
	{ "constinit",		CPPReserved.RID_CONSTINIT,	0 },
	{ "const_cast",		CPPReserved.RID_CONSTCAST,	0 },
	{ "continue",		CPPReserved.RID_CONTINUE,	0 },
	{ "decltype",       CPPReserved.RID_DECLTYPE,   0 },
	{ "default",		CPPReserved.RID_DEFAULT,	0 },
	{ "delete",			CPPReserved.RID_DELETE,	0 },
	{ "do",				CPPReserved.RID_DO,		0 },
	{ "double",			CPPReserved.RID_DOUBLE,	0 },
	{ "dynamic_cast",	CPPReserved.RID_DYNCAST,	0 },
	{ "else",			CPPReserved.RID_ELSE,	0 },
	{ "enum",			CPPReserved.RID_ENUM,	0 },
	{ "explicit",		CPPReserved.RID_EXPLICIT,	0 },
	{ "export",			CPPReserved.RID_EXPORT,	0 },
	{ "extern",			CPPReserved.RID_EXTERN,	0 },
	{ "false",			CPPReserved.RID_FALSE,	0 },
	{ "float",			CPPReserved.RID_FLOAT,	0 },
	{ "for",			CPPReserved.RID_FOR,	0 },
	{ "friend",			CPPReserved.RID_FRIEND,	0 },
	{ "goto",			CPPReserved.RID_GOTO,	0 },
	{ "if",				CPPReserved.RID_IF,		0 },
	{ "inline",			CPPReserved.RID_INLINE,	0 },
	{ "int",			CPPReserved.RID_INT,	0 },
	{ "long",			CPPReserved.RID_LONG,	0 },
	{ "mutable",		CPPReserved.RID_MUTABLE,	0 },
	{ "namespace",		CPPReserved.RID_NAMESPACE,	0 },
	{ "new",			CPPReserved.RID_NEW,	0 },
	{ "noexcept",		CPPReserved.RID_NOEXCEPT,	0 },
	{ "nullptr",		CPPReserved.RID_NULLPTR,	0 },
	{ "operator",		CPPReserved.RID_OPERATOR,	0 },
	{ "private",		CPPReserved.RID_PRIVATE,	0 },
	{ "protected",		CPPReserved.RID_PROTECTED,	0 },
	{ "public",			CPPReserved.RID_PUBLIC,	0 },
	{ "register",		CPPReserved.RID_REGISTER,	0 },
	{ "reinterpret_cast",	CPPReserved.RID_REINTCAST,	0 },
	{ "restrict",		CPPReserved.RID_RESTRICT,	0 },
	{ "return",			CPPReserved.RID_RETURN,	0 },
	{ "short",			CPPReserved.RID_SHORT,	0 },
	{ "signed",			CPPReserved.RID_SIGNED,	0 },
	{ "sizeof",			CPPReserved.RID_SIZEOF,	0 },
	{ "static",			CPPReserved.RID_STATIC,	0 },
	{ "static_assert",    	CPPReserved.RID_STATIC_ASSERT, 0 },
	{ "static_cast",	CPPReserved.RID_STATCAST,	0 },
	{ "struct",			CPPReserved.RID_STRUCT,	0 },
	{ "switch",			CPPReserved.RID_SWITCH,	0 },
	{ "template",		CPPReserved.RID_TEMPLATE,	0 },
	{ "this",			CPPReserved.RID_THIS,	0 },
	{ "thread_local",	CPPReserved.RID_THREAD,	0 },
	{ "throw",			CPPReserved.RID_THROW,	0 },
	{ "true",			CPPReserved.RID_TRUE,	0 },
	{ "try",			CPPReserved.RID_TRY,	0 },
	{ "typedef",		CPPReserved.RID_TYPEDEF,	0 },
	{ "typename",		CPPReserved.RID_TYPENAME,	0 },
	{ "typeid",			CPPReserved.RID_TYPEID,	0 },
	{ "typeof",			CPPReserved.RID_TYPEOF,	0 },
	{ "typeof_unqual",	CPPReserved.RID_TYPEOF_UNQUAL,	0 },
	{ "union",			CPPReserved.RID_UNION,	0 },
	{ "unsigned",		CPPReserved.RID_UNSIGNED,	0 },
	{ "using",			CPPReserved.RID_USING,	0 },
	{ "virtual",		CPPReserved.RID_VIRTUAL,	0 },
	{ "void",			CPPReserved.RID_VOID,	0 },
	{ "volatile",		CPPReserved.RID_VOLATILE,	0 },
	{ "wchar_t",		CPPReserved.RID_WCHAR,	0 },
	{ "while",			CPPReserved.RID_WHILE,	0 },
]

c_syntax = [
	# Function definition, if got numbers, can skip, as long as it is not starting with numbers
	{CPPType.CPP_NAME, CPPType.CPP_WHITESPACE, CPPType.CPP_NAME, CPPType.CPP_WHITESPACE or CPPType.CPP_OPEN_PAREN}
]

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

	return arr_arr

	print()
	print(string)
	for arr in arr_arr:
		print(arr)

def group_lex(string, cpp_option):
	"""
	given a string, with each token lexed
	eg: int8 main()
	i -> CPP_NAME
	n -> CPP_NAME
	t -> CPP_NAME
	8 -> CPP_NUMBER
	make it like
	int8 -> CPP_NAME
	main -> CPP_NAME
	() -> CPP_PARENTHESIS
	"""
	group_lex = []
	temp_string = ''
	wait_for_breaker = False
	arr_type = -1
	to_group_cpp_name = False
	to_group_parenthesis = False
	to_group_bracket = False

	arr_arr = lex_string(string, cpp_option)

	for arr in arr_arr:
		if arr['type'] == CPPType.CPP_NAME:
			to_group_cpp_name = True
		elif arr['type'] == CPPType.CPP_OPEN_PAREN:
			to_group_parenthesis = True
		elif arr['type'] == CPPType.CPP_OPEN_BRACE:
			to_group_bracket = True

		# Group CPP_NAME
		if 	to_group_cpp_name and\
			to_group_parenthesis == False and\
			to_group_bracket == False:
			if arr['type'] == CPPType.CPP_WHITESPACE:
				group_lex.append(
					{
						'word': temp_string,
						'type': arr_type
					}
				)
				arr_type = -1
				temp_string = ''
				wait_for_breaker = False
				to_group_cpp_name = False
				continue

			if arr['type'] == CPPType.CPP_OPEN_PAREN:
				group_lex.append(
					{
						'word': temp_string,
						'type': arr_type
					}
				)
				arr_type = -1
				temp_string = ''
				wait_for_breaker = False
				to_group_cpp_name = False
				pass

			if to_group_cpp_name:
				temp_string += arr['char']

				if wait_for_breaker == True:
					continue

				if 	arr['type'] == CPPType.CPP_NAME:
					if arr_type == -1: # to protect this variable being overwritten everytime
						arr_type = arr['type']
					wait_for_breaker = True
					continue

		# Group PARANTHESIS & BRACKET SCOPE
		if 	to_group_parenthesis or\
			to_group_bracket:
			temp_string += arr['char']

			if arr['type'] == CPPType.CPP_WHITESPACE:
				continue

			if arr['type'] == CPPType.CPP_CLOSE_PAREN or \
				arr['type'] == CPPType.CPP_CLOSE_BRACE:
				group_lex.append(
					{
						'word': temp_string,
						'type': arr_type
					}
				)
				arr_type = -1
				temp_string = ''
				wait_for_breaker = False
				to_group_cpp_name = False
				to_group_bracket = False
				to_group_parenthesis = False
				continue

			if wait_for_breaker == True:
				continue

			if arr['type'] == CPPType.CPP_OPEN_PAREN or \
				arr['type'] == CPPType.CPP_OPEN_BRACE:
				if arr_type != -1: # to protect this variable being overwritten everytime
					continue
				if arr['type'] == CPPType.CPP_OPEN_PAREN:
					arr_type = CPPType.CPP_PARENTHESIS
				elif arr['type'] == CPPType.CPP_OPEN_BRACE:
					arr_type = CPPType.CPP_BRACE
				wait_for_breaker = True
				continue

	for lex in group_lex:
		print(lex)
	print()

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
