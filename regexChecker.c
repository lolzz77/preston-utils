#include <stdio.h>
// How to run
// ./regexCheckerExe
// Then it will output 0 or 1
// 0 == match
// 1 == NOT MATCH

//clang 3.8.0

#include  <stdio.h>
#include  <regex.h>

#define PATTERN     "^[ ]*[a-zA-Z0-9()_*]+[ ]+[a-zA-Z0-9()_*]+[[]*[0-9]+[]]*[ ]*=[ ]*[{ ]*[^}]*[}]"
#define STRING      "ret = test();"

int main(void)
{
	printf("MEE %s:%s:%d\r\n", __FILE__, __FUNCTION__, __LINE__);

    char    *regPatt = regPatt = PATTERN;
   regex_t  regex;
   short    retval = regcomp (&regex, regPatt, REG_EXTENDED);
    short    status = regexec (&regex, STRING, (size_t) 0, NULL, 0);

   printf ("%hd\n", status);

   regfree (&regex);
}

/*
    LIST OF WEIRD THINGS TO FILTER OUT

1. return get_id(),


2. return get_ID(addr) &&

        get_ID(addr) &&

        get_ID(addr) &&

        get_ID(addr) &&

        get_ID(addr) &&

3.  return get_ID(addr) ?

4.     DINCParameterOption::DINCParameterOption( DINCParameterName_t inDINCParamName, int16_t * inDINCParamValuePtr )
	// {{{RME tool 'OT::Cpp' property 'ConstructorInitializer'
	// {{{USR

	// }}}USR
	// }}}RME
    {
        ...
    }

5.  // {{{RME classifier 'Logical View::Gemstones::OptionEvents::Microphone::Microphone Options::DINCParameterOption'

6. auto generated files
    search "AUTO GENERATED" keyword in opengrok

7.  void func() {...};
    
8.  void func(
        param1,
        param2,
    ) {...};

9.  void func (...) {
        ...
    }

10. void func (arr{}, arr[]) {
        ...
    }

11. void func (param = auto default value) {
        ...
    }

12. void func (...) 
    {
       ...
    }
    
    void func (
       ...
    ) {
       ...
    }
    void func (
       ...
    ) 
    {
       ...
    }
    
    void func
    (...) {
       ...
    }
    void func
    (...) 
    {
       ...
    }

13.  Class::Class(int x)
    : ClassBase(CONSTANT),
      m_var(CONSTANT)
    {

14. static int FAST_FUNC funcName(char **argv)
    {

15. void func(int x){}
    - it will result writing AFTER "}" becuase fgets will make cursor to end of string

16. #if defined(DEBUG)

17. #if ENABLE_HUSH_GETOPTS
*/