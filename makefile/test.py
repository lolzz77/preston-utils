import unittest

# Matches ${...}, $(...)
variable_regex = r'\$[\(\{][a-zA-Z0-9_-]+[\)\}]'

# detect `endif` word, optional leading & trailing whitespace
endif_regex = r"^\s*endif\s*"

# detect target recipe, tested in python regex online
# Explanation:
# Must not start with (?!keywords), and comment
# Must not begin with whitespace
# Match anything in the bracket, one or more
# Optional whitespace
# Must ':'
# Cannot contain `=` after that
target_recipe_regex = r"^(?!#|export|ifeq|ifneq|else|endif)[^\s][a-zA-Z0-9$(){}\s*/_-]+\s*:[^=]"

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

# class RegexClass(unittest.TestCase):
#     def test_endif_regex(self):
#         test_cases = [
#             [#0
#                 [   # test case
#                     'i', 
#                     'int main()', 
#                     lex.CPPOption.NONE
#                 ],
#                 [   # test result
#                     {
#                         "char" : 'i',
#                         "flag" : lex.CPP_Flag.NONE,
#                         "type" : lex.CPPType.CPP_NAME
#                     }
#                 ]
#             ],
#         ]

#         # doing this way, it will output which test case failed
#         # 1st index is 0
#         for i, test_case in enumerate(test_cases):
#             test_result = lex.lex(test_case[0][0], test_case[0][1], test_case[0][2])
#             with self.subTest(i=i):
#                 self.assertEqual(
#                     Counter(test_result), 
#                     Counter(test_case[1][0])
#                 )

# if __name__ == '__main__':
#     unittest.main()

















