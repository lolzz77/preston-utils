# pip install nltk

import re
import unittest
from collections import Counter
import include
import lex


class LexTestCase(unittest.TestCase):
    def test_lex(self):
        test_cases = [
            [#0
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
            [#1
                [
                    '(', 
                    'int main()', 
                    lex.CPPOption.NONE
                ],
                [
                    {
                        "char" : '(',
                        "flag" : lex.CPP_Flag.NONE,
                        "type" : lex.CPPType.CPP_OPEN_PAREN
                    }
                ]
            ],
            [#2
                [
                    '.', 
                    '...', 
                    lex.CPPOption.NONE
                ],
                [
                    {
                        "char" : '.',
                        "flag" : lex.CPP_Flag.NONE,
                        "type" : lex.CPPType.CPP_ELLIPSIS
                    }
                ]
            ],
            [#3
                [
                    '.', 
                    '..', 
                    lex.CPPOption.NONE
                ],
                [
                    {
                        "char" : '.',
                        "flag" : lex.CPP_Flag.NONE,
                        "type" : lex.CPPType.CPP_DOT
                    }
                ]
            ],
            [#4
                [
                    ' ', 
                    'int main()', 
                    lex.CPPOption.NONE
                ],
                [
                    {
                        "char" : ' ',
                        "flag" : lex.CPP_Flag.NONE,
                        "type" : lex.CPPType.CPP_WHITESPACE
                    }
                ]
            ],
            [#5
                [
                    '\t', 
                    'int main()', 
                    lex.CPPOption.NONE
                ],
                [
                    {
                        "char" : '\t',
                        "flag" : lex.CPP_Flag.NONE,
                        "type" : lex.CPPType.CPP_WHITESPACE
                    }
                ]
            ],
            [#6
                [
                    '\'', 
                    'int main()', 
                    lex.CPPOption.NONE
                ],
                [
                    {
                        "char" : '\'',
                        "flag" : lex.CPP_Flag.NONE,
                        "type" : lex.CPPType.CPP_STRING_SINGLE_QUOTE
                    }
                ]
            ],
        ]

        # doing this way, it will output which test case failed
        # 1st index is 0
        for i, test_case in enumerate(test_cases):
            test_result = lex.lex(test_case[0][0], test_case[0][1], test_case[0][2])
            with self.subTest(i=i):
                self.assertEqual(
                    Counter(test_result), 
                    Counter(test_case[1][0])
                )

    def test_lex_string(self):
        test_cases = [
            [#0
                [   # test case
                    'int main()', 
                    lex.CPPOption.NONE
                ],
                [   # test result
                    {
                        "char" : 'i',
                        "flag" : lex.CPP_Flag.NONE,
                        "type" : lex.CPPType.CPP_NAME
                    },
                    {
                        "char" : 'n',
                        "flag" : lex.CPP_Flag.NONE,
                        "type" : lex.CPPType.CPP_NAME
                    },
                    {
                        "char" : 't',
                        "flag" : lex.CPP_Flag.NONE,
                        "type" : lex.CPPType.CPP_NAME
                    },
                    {
                        "char" : ' ',
                        "flag" : lex.CPP_Flag.NONE,
                        "type" : lex.CPPType.CPP_WHITESPACE
                    },
                    {
                        "char" : 'm',
                        "flag" : lex.CPP_Flag.NONE,
                        "type" : lex.CPPType.CPP_NAME
                    },
                    {
                        "char" : 'a',
                        "flag" : lex.CPP_Flag.NONE,
                        "type" : lex.CPPType.CPP_NAME
                    },
                    {
                        "char" : 'i',
                        "flag" : lex.CPP_Flag.NONE,
                        "type" : lex.CPPType.CPP_NAME
                    },
                    {
                        "char" : 'n',
                        "flag" : lex.CPP_Flag.NONE,
                        "type" : lex.CPPType.CPP_NAME
                    },
                    {
                        "char" : '(',
                        "flag" : lex.CPP_Flag.NONE,
                        "type" : lex.CPPType.CPP_OPEN_PAREN
                    },
                    {
                        "char" : ')',
                        "flag" : lex.CPP_Flag.NONE,
                        "type" : lex.CPPType.CPP_CLOSE_PAREN
                    },
                ]
            ],
            [#1
                [
                    '(...)', 
                    lex.CPPOption.NONE
                ],
                [
                    {
                        "char" : '(',
                        "flag" : lex.CPP_Flag.NONE,
                        "type" : lex.CPPType.CPP_OPEN_PAREN
                    },
                    {
                        "char" : '.',
                        "flag" : lex.CPP_Flag.NONE,
                        "type" : lex.CPPType.CPP_ELLIPSIS
                    },
                    {
                        "char" : '.',
                        "flag" : lex.CPP_Flag.NONE,
                        "type" : lex.CPPType.CPP_DOT
                    },
                    {
                        "char" : '.',
                        "flag" : lex.CPP_Flag.NONE,
                        "type" : lex.CPPType.CPP_DOT
                    },
                    {
                        "char" : ')',
                        "flag" : lex.CPP_Flag.NONE,
                        "type" : lex.CPPType.CPP_CLOSE_PAREN
                    },
                ]
            ],
            [#2
                [
                    'x != 2', 
                    lex.CPPOption.NONE
                ],
                [
                    {
                        "char" : 'x',
                        "flag" : lex.CPP_Flag.NONE,
                        "type" : lex.CPPType.CPP_NAME
                    },
                    {
                        "char" : ' ',
                        "flag" : lex.CPP_Flag.NONE,
                        "type" : lex.CPPType.CPP_WHITESPACE
                    },
                    {
                        "char" : '!',
                        "flag" : lex.CPP_Flag.NONE,
                        "type" : lex.CPPType.CPP_NOT_EQ
                    },
                    {
                        "char" : '=',
                        "flag" : lex.CPP_Flag.NONE,
                        "type" : lex.CPPType.CPP_EQ
                    },
                    {
                        "char" : ' ',
                        "flag" : lex.CPP_Flag.NONE,
                        "type" : lex.CPPType.CPP_WHITESPACE
                    },
                    {
                        "char" : '2',
                        "flag" : lex.CPP_Flag.NONE,
                        "type" : lex.CPPType.CPP_NUMBER
                    }
                ]
            ],
            # [#3
            #     [
            #         '#define ABC 123', 
            #         lex.CPPOption.NONE
            #     ],
            #     [
            #         {
            #             "char" : 'x',
            #             "flag" : lex.CPP_Flag.NONE,
            #             "type" : lex.CPPType.CPP_NAME
            #         },
            #     ]
            # ],
            # [#4
            #     [
            #         '#include <stdio.h>', 
            #         lex.CPPOption.NONE
            #     ],
            #     [
            #         {
            #             "char" : 'x',
            #             "flag" : lex.CPP_Flag.NONE,
            #             "type" : lex.CPPType.CPP_NAME
            #         },
            #     ]
            # ],
        ]

        for i, test_case in enumerate(test_cases):
            test_result = lex.lex_string(test_case[0][0], test_case[0][1])
            with self.subTest(i=i):
                self.assertEqual(
                    test_result, 
                    test_case[1]
                )


    def test_group_lex(self):
        test_cases = [
            [#0
                [   # test case
                    'int main(){}', 
                    lex.CPPOption.NONE
                ],
                [   # test result
                    {
                        "word" : 'int',
                        "flag" : lex.CPP_Flag.NONE,
                        "type" : lex.CPPType.CPP_NAME
                    },
                    {
                        "word" : ' ',
                        "flag" : lex.CPP_Flag.NONE,
                        "type" : lex.CPPType.CPP_WHITESPACE
                    },
                    {
                        "word" : 'main',
                        "flag" : lex.CPP_Flag.NONE,
                        "type" : lex.CPPType.CPP_NAME
                    },
                    {
                        "word" : '()',
                        "flag" : lex.CPP_Flag.NONE,
                        "type" : lex.CPPType.CPP_PARENTHESIS
                    },
                    {
                        "word" : '{}',
                        "flag" : lex.CPP_Flag.NONE,
                        "type" : lex.CPPType.CPP_BRACE
                    },
                ]
            ],
            [#1
                [
                    'int main () {}', 
                    lex.CPPOption.NONE
                ],
                [
                ]
            ],
            [#2
                [
                    'int main ( ) { }', 
                    lex.CPPOption.NONE
                ],
                [
                ]
            ],
            [#3
                [
                    'int main (int x, int y) {int x, int y}', 
                    lex.CPPOption.NONE
                ],
                [
                ]
            ],
            [#4
                [
                    'int * main() {}', 
                    lex.CPPOption.NONE
                ],
                [
                ]
            ],
            [#5 i think is okay that it treats int& as CPP_NAME, dont think split it helps me.
                [
                    'int* main() {}', 
                    lex.CPPOption.NONE
                ],
                [
                ]
            ],
            [#6
                [
                    'int & main() {}', 
                    lex.CPPOption.NONE
                ],
                [
                ]
            ],
            [#7 i think is okay that it treats int& as CPP_NAME, dont think split it helps me.
                [
                    'int& main() {}', 
                    lex.CPPOption.NONE
                ],
                [
                ]
            ],
            [#8
                [
                    '__cold int * main ( ) { int x; int y; while(x) {printf("Hello world!")} }', 
                    lex.CPPOption.NONE
                ],
                [
                ]
            ],
            [#9
                [
                    '__cold int * main ( int x[], int y(), int z{5, 6, 7} ) { int x; int y; while(x) {printf("Hello world!")} }', 
                    lex.CPPOption.NONE
                ],
                [
                ]
            ],
            [#10
                [
                    '__cold (int) (*) main ( ) { }', 
                    lex.CPPOption.NONE
                ],
                [
                ]
            ],
            [#11
                [
                    '__cold (int) (&) main ( ) { }', 
                    lex.CPPOption.NONE
                ],
                [
                ]
            ],
            [#12 i think is okay that it treats (int&) as PARENTHESIS, cos how u wanna split? It's inside parenthesis
                [
                    '__cold (int*) main ( ) { }', 
                    lex.CPPOption.NONE
                ],
                [
                ]
            ],
            [#13 i think is okay that it treats (int&) as PARENTHESIS, cos how u wanna split? It's inside parenthesis
                [
                    '__cold (int&) main ( ) { }', 
                    lex.CPPOption.NONE
                ],
                [
                ]
            ],
        ]

        # for i, test_case in enumerate(test_cases):
            # print(i)
            # test_result = lex.group_lex(test_case[0][0], test_case[0][1])
            # with self.subTest(i=i):
                # self.assertEqual(
                #     test_result, 
                #     test_case[1]
                # )


    def test_detect_keyword(self):
        test_cases = [
            [#0
                [   # test case
                    {
                        'word':'int',
                        'type': lex.CPPType.CPP_NAME,
                        'flag': lex.CPP_Flag.NONE,
                    },
                    {
                        'word':'main',
                        'type': lex.CPPType.CPP_NAME,
                        'flag': lex.CPP_Flag.NONE,
                    },
                    {
                        'word':'()',
                        'type': lex.CPPType.CPP_PARENTHESIS,
                        'flag': lex.CPP_Flag.NONE,
                    },
                    {
                        'word':'{}',
                        'type': lex.CPPType.CPP_BRACE,
                        'flag': lex.CPP_Flag.NONE,
                    },
                ],
                [   # test result
                ]
            ],
            [#2
                [
                    {
                        'word':'int',
                        'type': lex.CPPType.CPP_NAME,
                        'flag': lex.CPP_Flag.NONE,
                    },
                    {
                        'word':'*',
                        'type': lex.CPPType.CPP_MULT,
                        'flag': lex.CPP_Flag.NONE,
                    },
                    {
                        'word':'_Decimal64',
                        'type': lex.CPPType.CPP_NAME,
                        'flag': lex.CPP_Flag.NONE,
                    },
                    {
                        'word':'main',
                        'type': lex.CPPType.CPP_NAME,
                        'flag': lex.CPP_Flag.NONE,
                    },
                    {
                        'word':'( int x, int y )',
                        'type': lex.CPPType.CPP_PARENTHESIS,
                        'flag': lex.CPP_Flag.NONE,
                    },
                    {
                        'word':'{ x = 5; while(x) {printf("Hello"\r\n)} }',
                        'type': lex.CPPType.CPP_BRACE,
                        'flag': lex.CPP_Flag.NONE,
                    },
                ],
                [
                ]
            ]
        ]

        for i, test_case in enumerate(test_cases):
            print(i)
            test_result = lex.detect_keyword(test_case[0])
            # with self.subTest(i=i):
                # self.assertEqual(
                #     test_result, 
                #     test_case[1]
                # )


if __name__ == '__main__':
    unittest.main()

















