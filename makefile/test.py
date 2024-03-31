import unittest
import re

# detect `endif` word, optional leading & trailing whitespace
endif_regex = r"^\s*endif\s*"

# Matches ${...}, $(...)
variable_regex = r"\$[\(\{][a-zA-Z0-9_-]+[\)\}]"

# detect target recipe, tested in python regex online
# Explanation:
# Must not start with (?!keywords), and comment
# Must not begin with whitespace
# Match anything in the bracket, one or more
# Optional whitespace
# Must ':'
# Cannot contain `=` after that
target_recipe_regex = r"^(?!#|export|ifeq|ifneq|else|endif)[^\s][a-zA-Z0-9$(){}\s*/_-]+\s*:[^=]"
# List of test
# ABC : DEF
#  ABC : DEF
# ABC :
# $(DSP): TAR
# ${GG}:
# abc-def:
# ABC $(ABC):
# ABC $(ABC) :
# $(ABC)/$(DEF)_$(GHI)_EFF:
# export ABC:=123
# ABC :=
# ABC : =   (For this one, 
#           it will match, and maekfile will not fail for typing like this, but dont worry,
#           if you type like this, the variable is not assigned, despite makefile still can run
# ABC =:
# #command: abc

# Matches variable
# eg: ABC=1, ABC:=1, export ABC=1
# Explanation:
# Must not start with comment
variable_regex_2 = r"^(?!#)[a-zA-Z0-9$(){}\s*/_-]+:*="
# List of test
# ARM : DSP
# ABC :
# $(DSP): TAR
# ${GG}:
# abc-def:
# DSP $(DSP):
# DSP $(DSP) :
# $(GEN)/$(target)_(fw)_OUT:
# export ABC :
# AXN : =
# AXN = :
# #COMMAND:
# ABC = 1
# ABC := 1
# ABC=1
# ABC:=1
# export ABC=1
#      ABC=1
# $(ABC)=1
# $(ABC):=1
# #ABC=1
#      #(ABC)=1



class RegexClass(unittest.TestCase):
    def test_endif_regex(self):
        regex_to_test = endif_regex
        test_cases = [
            [#0
                'endif',
                True,
            ],
            [#0
                'endif   ',
                True,
            ],
            [#1
                'abcendif',
                False,
            ],
            [#2
                '   abcendif',
                False,
            ],
            [#3
                '   abcendif   ',
                False,
            ],
            [#4
                '#endif',
                False,
            ],
            [#5
                '@endif',
                False,
            ],
        ]

        # For failed test case, it will print in the terminal
        # Look for keyword `FAIL:`
        for index, test_case in enumerate(test_cases):
            test_result = bool(re.search(regex_to_test, test_case[0]))
            with self.subTest(test_case=test_case):
                self.assertEqual(test_result, test_case[1], f"Failed test case at index {index-1}")


    def test_variable_regex(self):
        regex_to_test = variable_regex
        test_cases = [
            [#0
                '$(ABC)',
                True,
            ],
            [#0
                '    $(ABC)',
                True,
            ],
            [#1
                'export $(ABC)',
                True,
            ],
            [#2
                '# $(ABC)',
                True,
            ],
            [#3
                '${ABC}',
                True,
            ],
            [#4
                '    ${ABC}',
                True,
            ],
            [#5
                'export ${ABC}',
                True,
            ],
            [#6
                '# ${ABC}',
                True,
            ],
        ]

        for index, test_case in enumerate(test_cases):
            test_result = bool(re.search(regex_to_test, test_case[0]))
            with self.subTest(test_case=test_case):
                self.assertEqual(test_result, test_case[1], f"Failed test case at index {index-1}")

if __name__ == '__main__':
    unittest.main()

















