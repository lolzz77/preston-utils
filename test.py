# pip install nltk

import re
import unittest
from collections import Counter
import include
import lex


class LexTestCase(unittest.TestCase):
    def test_lex(self):
        test_cases = [
            [
                [   # test case
                    'i', 
                    'int main()', 
                    lex.CPPOption.NONE
                ],
                [   # test result
                    {
                        "char" : 'i',
                        "flag" : lex.CPP_Flag.NONE,
                        "type" : lex.CPPType.CPP_NAME
                    }
                ]
            ],
            [
                [   # test case
                    '(', 
                    'int main()', 
                    lex.CPPOption.NONE
                ],
                [   # test result
                    {
                        "char" : '(',
                        "flag" : lex.CPP_Flag.NONE,
                        "type" : lex.CPPType.CPP_OPEN_PAREN
                    }
                ]
            ],
            [
                [   # test case
                    '.', 
                    '...', 
                    lex.CPPOption.NONE
                ],
                [   # test result
                    {
                        "char" : '.',
                        "flag" : lex.CPP_Flag.NONE,
                        "type" : lex.CPPType.CPP_ELLIPSIS
                    }
                ]
            ],
        ]

        # doing this way, it will output which test case failed
        # 1st index is 0
        for i, test_case in enumerate(test_cases):
            test_result = {}
            test_result = lex.lex(test_case[0][0], test_case[0][1], test_case[0][2])
            with self.subTest(i=i):
                self.assertEqual(
                    Counter(test_result), 
                    Counter(test_case[1][0])
                )

if __name__ == '__main__':
    unittest.main()

















