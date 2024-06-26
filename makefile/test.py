import unittest
import re
import inspect
import os
import subprocess

# detect `endif` word, optional leading & trailing whitespace
endif_regex = r"^\t*endif\t*"

# Matches ${...}, $(...)
# Note :
# For this one, it is caller diligence to make sure the line is not a comment line
# Explanation :
# Can start with whitepsace
# But 1st character, cannot start with `#`, the comment
# Then matches anything except $ and #, for cases like `export $(ABC)`
# Then, matches $( or ${
# Then, anything in the bracket
# Then, ) or }
variable_regex = r"\$[\(\{][a-zA-Z0-9_-]+[\)\}]"

# detect target recipe, tested in python regex online
# Explanation:
# Must not start with (?!keywords)
# Must not begin with whitespace
# Match anything in the bracket, one or more
# Optional whitespace
# Must ':'
# Cannot contain `=` after that
target_recipe_regex = r"^(?!export|ifeq|ifneq|else|endif|\s)[a-zA-Z0-9$\(\)\{\}\s\/_-]+\s*:[^=]"

# Matches variable
# eg: ABC=1, ABC:=1, export ABC=1
# Explanation:
# start with anything, then must match either `:=` or `=` or `?=`
# Cannot be `==` at the end, must only be 1 `=` only
assigned_variable_regex = r"[a-zA-Z0-9$(){}/_-]+\s*[+:?]?=(?!=)"


class TestClass(unittest.TestCase):
    def test_endif_regex(self):
        regex_to_test = endif_regex
        test_cases = [
            [#0
                'endif',
                True,
            ],
            [#1
                'endif   ',
                True,
            ],
            [#2
                'abcendif',
                False,
            ],
            [#3
                '   abcendif',
                False,
            ],
            [#4
                '   abcendif   ',
                False,
            ],
            [#5
                '#endif',
                False,
            ],
            [#6
                '@endif',
                False,
            ],
            [#7
                """newline
                endif""",
                False,
            ],
        ]

        for index, test_case in enumerate(test_cases):
            test_result = bool(re.search(regex_to_test, test_case[0]))
            with self.subTest(test_case=test_case):
                self.assertEqual(test_result, test_case[1], f"Line {inspect.currentframe().f_lineno} : Test Case {index}")


    def test_variable_regex(self):
        regex_to_test = variable_regex
        test_cases = [
            [#0
                're.search',
                '$(ABC)',
                True,
            ],
            [#1
                're.search',
                '    $(ABC)',
                True,
            ],
            [#2
                're.search',
                'export $(ABC)',
                True,
            ],
            [#3
                're.search',
                '# $(ABC)',
                True,
            ],
            [#4
                're.search',
                '${ABC}',
                True,
            ],
            [#5
                're.search',
                '    ${ABC}',
                True,
            ],
            [#6
                're.search',
                'export ${ABC}',
                True,
            ],
            [  #7
                're.search',
                '# ${ABC}',
                True,
            ],
            [  #8
                're.findall',
                'export ${ABC} $(DEF)',
                ['${ABC}', '$(DEF)'],
            ],
        ]

        for index, test_case in enumerate(test_cases):
            if test_case[0] == 're.findall':
                test_result = re.findall(regex_to_test, test_case[1])
            else: #re.search
                test_result = bool(re.search(regex_to_test, test_case[1]))
            with self.subTest(test_case=test_case):
                self.assertEqual(test_result, test_case[2], f"Line {inspect.currentframe().f_lineno} : Test Case {index}")


    def test_target_recipe_regex(self):
        regex_to_test = target_recipe_regex
        # Note: All the test cases here must end with newline
        # Cos, target recipe confirm must end with newline
        test_cases = [
            [#0
                'ARS : WER \
                ',
                True,
            ],
            [#1
                'ABC : \
                ',
                True,
            ],
            [#2
                '$(AFS): TAR \
                ',
                True,
            ],
            [#3
                '${GG}: \
                ',
                True,
            ],
            [#4
                'abc-def: \
                ',
                True,
            ],
            [#5
                'QQQ $(QQQ): \
                ',
                True,
            ],
            [#6
                'QQQ $(QQQ) : \
                ',
                True,
            ],
            [#7
                '$(GEN)/$(VAR)_(abc)_DEF: \
                ',
                True,
            ],
            [#8
                'export ABC : 123 \
                ',
                False,
            ],
            [#9
                'export ABC := 123 \
                ',
                False,
            ],
            [#10
                'AXN := \
                ',
                False,
            ],
            [#11
                'AXN = : \
                ',
                False,
            ],
            [#12
                'AXN =: \
                ',
                False,
            ],
            [#13
                # The main.py script will handle commented code
                # that is, this test is not important,
                # it will not affect how the program behaves
                # Expected result should be True, 
                # But because i didnt put [a-zA-Z0-9#] ('#' in the bracket)
                # Thus, the result will be False
                '#COMMAND: \
                ',
                False,
            ],
            [#14
                # The main.py script will handle commented code
                # that is, this test is not important,
                # it will not affect how the program behaves
                # Expected result should be True, 
                # But because i didnt put [a-zA-Z0-9#] ('#' in the bracket)
                # Thus, the result will be False
                '#COMMAND:abc \
                ',
                False,
            ],
            [#15
                'ABC = 1 \
                ',
                False,
            ],
            [#16
                'ABC := 1 \
                ',
                False,
            ],
            [#17
                'ABC=1 \
                ',
                False,
            ],
            [#18
                'ABC:=1 \
                ',
                False,
            ],
            [#19
                'export ABC=1 \
                ',
                False,
            ],
            [#20
                '     ABC=1 \
                ',
                False,
            ],
            [#21
                '$(ABC)=1 \
                ',
                False,
            ],
            [#22
                '$(ABC):=1 \
                ',
                False,
            ],
            [#23
                '#ABC=1 \
                ',
                False,
            ],
            [#24
                '     #(ABC)=1 \
                ',
                False,
            ],
            [#25
                'all: $(ABC) $(DEF)  \
                ',
                True,
            ],
            # [#26
            #     # TODO: need fix this?
            #     # This is invalid syntax in makefile,
            #     # Tho makefile will not fail, but the makefile output will be not expected
            #     'AXN : = \
            #     ',
            #     False,
            # ],
        ]

        for index, test_case in enumerate(test_cases):
            test_result = bool(re.search(regex_to_test, test_case[0]))
            with self.subTest(test_case=test_case):
                self.assertEqual(test_result, test_case[1], f"Line {inspect.currentframe().f_lineno} : Test Case {index}")

    def test_assigned_variable_regex(self):
        regex_to_test = assigned_variable_regex
        # Note: All the test cases here must end with newline
        # Cos, target recipe confirm must end with newline
        test_cases = [
            [#0
                're.search',
                'ARS : WER \
                ',
                False,
            ],
            [#1
                're.search',
                'ABC : \
                ',
                False,
            ],
            [#2
                're.search',
                '$(AFS): TAR \
                ',
                False,
            ],
            [#3
                're.search',
                '${GG}: \
                ',
                False,
            ],
            [#4
                're.search',
                'abc-def: \
                ',
                False,
            ],
            [#5
                're.search',
                'QQQ $(QQQ): \
                ',
                False,
            ],
            [#6
                're.search',
                'QQQ $(QQQ) : \
                ',
                False,
            ],
            [#7
                're.search',
                '$(GEN)/$(VAR)_(abc)_DEF: \
                ',
                False,
            ],
            [#8
                're.search',
                'export ABC : 123 \
                ',
                False,
            ],
            [#9
                're.search',
                'export ABC := 123 \
                ',
                True,
            ],
            [#10
                're.search',
                'AXN := \
                ',
                True,
            ],
            [#11
                # TODO: need fix this?
                # This is invalid syntax in makefile,
                # Tho makefile will not fail, but the makefile output will be not expected
                're.search',
                'AXN : = \
                ',
                False,
            ],
            [#12
                're.search',
                'AXN = : \
                ',
                True,
            ],
            [#13
                're.search',
                'AXN =: \
                ',
                True,
            ],
            [#14
                # The script will handle commented code
                're.search',
                '#COMMAND: \
                ',
                False,
            ],
            [#15
                # The script will handle commented code
                're.search',
                '#COMMAND:abc \
                ',
                False,
            ],
            [#16
                # The script will handle commented code
                're.search',
                '#COMMAND:=abc \
                ',
                True,
            ],
            [#17
                # The script will handle commented code
                're.search',
                '#COMMAND=abc \
                ',
                True,
            ],
            [#18
                're.search',
                'ABC = 1 \
                ',
                True,
            ],
            [#19
                're.search',
                'ABC := 1 \
                ',
                True,
            ],
            [#20
                're.search',
                'ABC=1 \
                ',
                True,
            ],
            [#21
                're.search',
                'ABC:=1 \
                ',
                True,
            ],
            [#22
                're.search',
                'export ABC=1 \
                ',
                True,
            ],
            [#23
                're.search',
                '     ABC=1 \
                ',
                True,
            ],
            [#24
                're.search',
                '$(ABC)=1 \
                ',
                True,
            ],
            [#25
                're.search',
                '$(ABC):=1 \
                ',
                True,
            ],
            [#26
                're.search',
                '#ABC=1 \
                ',
                True,
            ],
            [#27
                're.search',
                '     #(ABC)=1 \
                ',
                True,
            ],
            [#28
                're.findall',
                'export ABC=1 \
                ',
                ['ABC='],
            ],
            [#29
                're.findall',
                '_abc=$(call AAD, VAR1, VAR2) \
                ',
                ['_abc='],
            ],
            [#30
                're.searchOne',
                '_abc = var1=2 \
                ',
                '_abc =',
            ],
            [#31
                're.search',
                '$(SILENCE)$(ECHO) ====== \
                ',
                False,
            ],
            [#32
                're.search',
                ' $(ABC) ?= 1 \
                ',
                True,
            ],
            [#33
                're.search',
                ' ABC ?= 1 \
                ',
                True,
            ],
            [#34
                're.search',
                ' export ABC ?= 1 \
                ',
                True,
            ],
            [#35
                're.search',
                'ABC += 1 \
                ',
                True,
            ],
            [#36
                're.searchOne',
                'ABC += 1 \
                ',
                'ABC +=',
            ],
            [#37
                're.searchOne',
                'ABC := 1 \
                ',
                'ABC :=',
            ],
            [#38
                're.searchOne',
                'ABC ?= 1 \
                ',
                'ABC ?=',
            ],
            # [#36
            #     # TODO: how to fix?
            #     're.search',
            #     '$(ABC)$(DEF) "Note: var=no." \
            #     ',
            #     False,
            # ],
        ]

        for index, test_case in enumerate(test_cases):
            if test_case[0] == 're.findall':
                test_result = re.findall(regex_to_test, test_case[1])
            elif test_case[0] == 're.searchOne':
                test_result = re.search(regex_to_test, test_case[1])
                test_result = test_result.group()
            else: #re.search
                test_result = bool(re.search(regex_to_test, test_case[1]))

            with self.subTest(test_case=test_case):
                self.assertEqual(test_result, test_case[2], f"Line {inspect.currentframe().f_lineno} : Test Case {index}")



    def test_makefile_1(self):
        """
        Makefile to test : Makefile1.mk
        Argument to pass in : "VAR1=1
        eg : this unit test will run command `python3 /data/preston-utils/makefile/main.py /data/preston-utils/makefile/test/Makefile1.mk "VAR1=1"
        """
        makefile_1_path = ''
        python_script = ''

        test_py_path = os.path.abspath(__file__)
        directory = os.path.dirname(test_py_path)
        makefile_1_test_output_path = directory + '/test_output/Makefile1_output.mk'
        makefile_1_test_output_readlines = []

        makefile_1_output_path = ''
        makefile_1_output_readlines = []

        python_script = directory + '/main.py'
        makefile_1_path = directory + '/test/Makefile1.mk'
        command = "python3" + ' ' + python_script + ' ' + makefile_1_path + ' ' + '"VAR1=1"'

        output = subprocess.check_output(command, shell=True)
        output_list = output.decode("utf-8").split('\n')
        makefile_1_output_path = output_list[0]
        makefile_1_output_path = makefile_1_output_path[len('Output: '):]

        with open(makefile_1_output_path, 'r') as file:
            makefile_1_output_readlines = file.readlines()

        with open(makefile_1_test_output_path, 'r') as file:
            makefile_1_test_output_readlines = file.readlines()

        self.assertEqual(makefile_1_output_readlines, makefile_1_test_output_readlines, "Makefile1.mk failed")
        
    def test_makefile_2(self):
        """
        Makefile to test : Makefile2.mk
        Argument to pass in : "VAR1=1
        eg : this unit test will run command `python3 /data/preston-utils/makefile/main.py /data/preston-utils/makefile/test/Makefile2.mk "VAR1=1"
        """
        makefile_2_path = ''
        python_script = ''

        test_py_path = os.path.abspath(__file__)
        directory = os.path.dirname(test_py_path)
        makefile_2_test_output_path = directory + '/test_output/Makefile2_output.mk'
        makefile_2_test_output_readlines = []

        makefile_2_output_path = ''
        makefile_2_output_readlines = []

        python_script = directory + '/main.py'
        makefile_2_path = directory + '/test/Makefile2.mk'
        command = "python3" + ' ' + python_script + ' ' + makefile_2_path + ' ' + '"VAR1=1"'
        
        output = subprocess.check_output(command, shell=True)
        output_list = output.decode("utf-8").split('\n')
        makefile_2_output_path = output_list[0]
        makefile_2_output_path = makefile_2_output_path[len('Output: '):]

        with open(makefile_2_output_path, 'r') as file:
            makefile_2_output_readlines = file.readlines()

        with open(makefile_2_test_output_path, 'r') as file:
            makefile_2_test_output_readlines = file.readlines()

        self.assertEqual(makefile_2_output_readlines, makefile_2_test_output_readlines, "Makefile2.mk failed")


if __name__ == '__main__':
    unittest.main()

















