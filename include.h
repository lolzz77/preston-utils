#include <regex.h>
#include <glob.h>
#include <ctype.h>

#define LIB_TO_WRITE                    "#include <stdio.h>\n" \
                                        "#include <pthread.h>\n"

#define COLOR_RESET         "\\x1b[0m"
#define COLOR_UNDERLINE     "\\x1b[4m"
#define COLOR_REVERSE       "\\x1b[7m"
#define COLOR_RED           "\\x1b[31m"
#define COLOR_GREEN         "\\x1b[32m"
#define COLOR_YELLOW        "\\x1b[33m"
#define COLOR_BLUE          "\\1b[34m"
#define COLOR_MAGENTA       "\\x1b[35m"
#define COLOR_CYAN          "\\x1b[36m"
#define COLOR_WHITE         "\\x1b[37m"
#define COLOR_GREY          "\\x1b[90m"
#define COLOR_LIGHTRED      "\\x1b[1;31m"
#define COLOR_LIGHTGREEN    "\\x1b[1;32m"
#define COLOR_LIGHTYELLOW   "\\x1b[1;33m"
#define COLOR_LIGHTBLUE     "\\x1b[1;34m"
#define COLOR_LIGHTMAGENTA  "\\x1b[1;35m"
#define COLOR_LIGHTCYAN     "\\x1b[1;36m"

char **stack = NULL;
int stack_size = 1;
int stack_top = 0;

char* POSIX_regex_match[] = {
        // for constructor & destructor, they dont have function return type
        // so basically they are already filtered out
/*0*/  "^[ (]*[a-zA-Z0-9_*]+[ &*]*[ )]*[ ]+[a-zA-Z0-9_*]+[ ]*\\([^{)]*[)]*[ ]*", // void test() || void * test() || (void *) test()

        /*  Attention to [16]
            You cannot [ ]*[(][^{)]*[)][ ]*
            for cases like
            static D_UINT32 decodeCorrectedBits(
                FFXIOSTATUS    *pIoStat)
            {
            will fail

            You have to [ ]*\\([^{)]*\\)[ ]*

            You do not need to escape the ( and ) characters when they appear 
            inside a character set enclosed in square brackets [ ]. 
            Within a character set, the ( and ) characters lose their 
            special meanings and are treated as literal characters.

            Update, cannot [ ]*\\([^{)]*\\)[ ]*
            for cases like
            unsigned char* display_get_bitmap_buffer(char* string, unsigned int num_chars,
                                         unsigned int width, unsigned int height,
                                         top_font_info_t* font_info)
            {
            will fail

            you have to [ ]*\\([^{)]*[)]*[ ]*
        */
/*1*/  "^[ (]*[a-zA-Z0-9_*]+[ &*]*[ )]*[ ]+[a-zA-Z0-9_*]+[ ]+[a-zA-Z0-9_*]+[ ]*\\([^{)]*[)]*[ ]*", // void __static test() || void * __static test() || (void *) __static test()
/*2*/  "^[ ]*[a-zA-Z0-9_*]+[ ]+[ (]*[a-zA-Z0-9_*]+[ &*]*[) ]*[ ]+[a-zA-Z0-9_*]+[ ]+[a-zA-Z0-9_*]+[ ]*\\([^{)]*[)]*[ ]*", // static/extern int FAST_FUNC test() || static (int *) FAST_FUNC test()
        // You cannot put [::], the regex treat it as match any that is defined in the group/bracket 
        // You have to just ::
/*3*/  "^[ (]*[a-zA-Z0-9_*]+[ &*]*[ )]*[ ]+[a-zA-Z0-9_*]+[ ]*::[ ]*[a-zA-Z0-9_*]+[ ]*\\([^{)]*[)]*[ ]*", // void class::func() || void * class::func() || void & class::func()
};

char* POSIX_regex_no_match[] = {
        /* If matches these, skip */
/*0*/   "^[ ]*inline",
/*1*/   "^[ ]*[#][ ]*define",
/*2*/   "^[ ]*[#][ ]*if[ ]+[(]*defined",
/*3*/   "^[ ]*[#][ ]*if[(]*defined", //dk why [if][ ]+ will fail
/*4*/   "^[ ]*[#][ ]*ifndef",

        /*
            In C regex_comp, () has special meaning
            They are used to group subexpressions within a larger expression
            you have to use double backslahses to escape that

            same goes to {}
            For example, the regular expression a{3} matches the character a repeated exactly 3 times.
        */
/*5*/   "^[ ]*if[ ]*\\(",
/*6*/   "^[ ]*else[ ]*\\{",
/*7*/   "^[ ]*else if[ ]*\\(",
/*8*/   "^[ ]*switch[ ]*\\(",
/*9*/   "^[ ]*case[ ]*[^:]+[ ]*:",
/*10*/  "^[ ]*return[ ]*[^;]+[ ]*[;?,&&|]",
/*11*/  "^[ ]*typedef[ ]*",
/*12*/  "^[ ]*union[ ]*",

        // They are relatively safe cause '^' indicate start of string must be 'for' 'do' 'while' etc.
        // A function would start at 'void' 'int' 'char' etc, never start at 'for' 'do' 'while' etc
        // So the following regex will not unintentionally skip the function
/*13*/   "^[ ]*for[ ]*\\(",
/*14*/   "^[ ]*do[ {]*", 
/*15*/   "^[ ]*while[ ]*\\(",

/*16*/  "^[ (]*[a-zA-Z0-9()_*]+[)]*[ ][a-zA-Z0-9_*]+[ ]*::[ ]*operator", // void class::operator >>&|<<
/*17*/  "^[a-zA-Z0-9_*]+::[~a-zA-Z0-9_*]+[ (]+", // class::class || class::~class constructor & destructor
/*18*/  "^[ ]*[a-zA-Z0-9()_*]+[ ]+[a-zA-Z0-9()_*]+[[]*[0-9]+[]]*[ ]*=[ ]*[{ ]*[^}]*[}]", // UINT32 UnifiedLogger_LL[1] = {(uintptr_t)vr_get_file_size};
};

char* filetype_to_work[] = {
    ".c",
    ".cpp",
};

// if you keep getting error n dont know how to solve, try make clean and rebuild, sometimes dif error comes out
char* exclude_dir_and_files[] = {
    ".",
    "..",
    ".git",
    ".repo",
    ".gitignore"
};

char* include_dir[] = {
    ""
};

// Struct to keep tract the file belongs to which parent path (eg trbo_l2boot, trbo_l3boot)
// So when i exclude the file, i only exclude it if it matches the parent path, i scare FW has similar file name and it get excluded
struct File{
    char* parent_path;
    char* file_or_path[10]; // no choice, have to hard code a size. Else u get error: initialization of flexible array member in a nested context
    char* func[10];
};

// List of functions to exlude to putting logs, it will cause radio crash
struct File exclude_func[] = {
    {
        "trbo_l3boot",
        {
            // leave it empty, dont initialize for this
        },
        {
            "reset_ram_init", // trbo_l3boot\L3\core\common\source\dsp\reset_dsp.c
        }
    },
};

// List of file to exlude to putting logs, it will cause radio crash
struct File exclude_file_or_path[] = {
    {
        "Folder A", 
        {
            "File/Folder A.c", 
        }
    },
    {
        "Folder B", 
        {
            "File/Folder B.c",
        }
    },
};

regex_t reegex_match,     reegex_match1,    reegex_match2,
        reegex_match3
        ;

regex_t reegex_no_match,     reegex_no_match1,    reegex_no_match2,
        reegex_no_match3,    reegex_no_match4,    reegex_no_match5,
        reegex_no_match6,    reegex_no_match7,    reegex_no_match8,
        reegex_no_match9,    reegex_no_match10,   reegex_no_match11,
        reegex_no_match12,   reegex_no_match13,   reegex_no_match14,
        reegex_no_match15,   reegex_no_match16,   reegex_no_match17,
        reegex_no_match18
        ;

#define SUCCESS 1
#define FAILURE -1
#define TRUE    1
#define FALSE   0

#define SKIP    20
#define IS_FILE 21
#define IS_DIR  22
#define UNKNOWN_ERROR -9
#define PROCEED 2
#define INVALID -99

#define ARR_SIZE(arr)                   sizeof(arr) / sizeof(arr[0])
#define MAX_READ_SIZE_PER_LINE          250 * 1024
#define MAX_ARR_SIZE                    256 * 2
#define CONSTRUCT_PATH_LEN(a, b, c)     (strlen(a) + strlen(b) + strlen(c))
#define TRBO_PATH                       "/trbo"
#define CURRENT_PATH                    "/"
#define GIT_IGNORE_FILE                 ".gitignore"
#define GIT_IGNORE_CMD                  "git check-ignore -v "
#define REGEX_FLAG                      REG_EXTENDED
// putting tab after each newline will cause progrma to append the whitespaces as well
/* previously...

char file_extension[256] = "\
.c|\
.cpp|\
.h";

*/
// Use #define instead of char* pointer. Since I dont want this to be in array. All in one single string
#define FILE_EXTENSION "[.c|.cpp]"
#define FILE_EXTENSION_MAKEFILE ".mk"

#define FLAGS_TO_DELETE "-Wall"

// wrapper for regex checking that DOESNT WANT to be matched
// return FALSE == a match that dont want to be matched is found
// return TRUE == otherwise
int no_match(const char* line_read, const char* file_path) {
    if 
    (
        (0 == regexec( &reegex_no_match, line_read, 0, NULL, 0))    ||
        (0 == regexec( &reegex_no_match1, line_read, 0, NULL, 0))   ||
        (0 == regexec( &reegex_no_match2, line_read, 0, NULL, 0))   ||
        (0 == regexec( &reegex_no_match3, line_read, 0, NULL, 0))   ||
        (0 == regexec( &reegex_no_match4, line_read, 0, NULL, 0))   ||
        (0 == regexec( &reegex_no_match5, line_read, 0, NULL, 0))   ||
        (0 == regexec( &reegex_no_match6, line_read, 0, NULL, 0))   ||
        (0 == regexec( &reegex_no_match7, line_read, 0, NULL, 0))   ||
        (0 == regexec( &reegex_no_match8, line_read, 0, NULL, 0))   ||
        (0 == regexec( &reegex_no_match9, line_read, 0, NULL, 0))   ||
        (0 == regexec( &reegex_no_match10, line_read, 0, NULL, 0))  ||
        (0 == regexec( &reegex_no_match11, line_read, 0, NULL, 0))  ||
        (0 == regexec( &reegex_no_match12, line_read, 0, NULL, 0))  ||
        (0 == regexec( &reegex_no_match13, line_read, 0, NULL, 0))  ||
        (0 == regexec( &reegex_no_match14, line_read, 0, NULL, 0))  ||
        (0 == regexec( &reegex_no_match15, line_read, 0, NULL, 0))  ||
        (0 == regexec( &reegex_no_match16, line_read, 0, NULL, 0))  ||
        (0 == regexec( &reegex_no_match17, line_read, 0, NULL, 0))  ||
        (0 == regexec( &reegex_no_match18, line_read, 0, NULL, 0))
    )
    {
        return FALSE;
    }
    
    // Check functions to exclude
    for (int i=0; i<ARR_SIZE(exclude_func); i++)
    {
        // Check if parent path matches
        if ((strstr(file_path, exclude_func[i].parent_path)))
        {
            // Loop thru each files and check if current function needs to be excluded
            for (int j=0; j<ARR_SIZE(exclude_func[i].func); j++)
            {
                // Since the struct has fixed size array, i have to check NULL, else segmentation fault
                if(NULL == exclude_func[i].func[j])
                    break;
                // The 'current function' that system is reading, is to be excluded
                if ((strstr(line_read, exclude_func[i].func[j])))
                    return FALSE;
            }
        }
    }

    // Check files to exclude
    for (int i=0; i<ARR_SIZE(exclude_file_or_path); i++)
    {
        // Check if parent path matches
        if ((strstr(file_path, exclude_file_or_path[i].parent_path)))
        {
            // Loop thru each files and check if current files need to be excluded
            for (int j=0; j<ARR_SIZE(exclude_file_or_path[i].file_or_path); j++)
            {
                // Since the struct has fixed size array, i have to check NULL, else segmentation fault
                if(NULL == exclude_file_or_path[i].file_or_path[j])
                    break;
                // The 'current file' that system is opening, is to be excluded
                if ((strstr(file_path, exclude_file_or_path[i].file_or_path[j])))
                    return FALSE;
            }
        }
    }
    
    return TRUE;
}

// wrapper for regex checking that wants to be matched
int match(const char* line_read) {
    if 
    (
        (0 == regexec( &reegex_match, line_read, 0, NULL, 0)) ||
        (0 == regexec( &reegex_match1, line_read, 0, NULL, 0)) ||
        (0 == regexec( &reegex_match2, line_read, 0, NULL, 0)) ||
        (0 == regexec( &reegex_match3, line_read, 0, NULL, 0))
    )
    {
        return TRUE;
    }
    return FALSE;
}

/*
    For cases like
    int x = 5; //comment here
*/ 
int is_within_comment(const char* line_read, const char* STRING) {
    // This is for cases like, the comment is after the code
    // eg: int x; // the func() bla bla bla
    // Here, if the code detected func() exists, it will write the log
    // But the thing is, the func() is in a comment line, so in this case, skip

    // check if contain comment symbol
    if(strstr(line_read, "//"))
    {
        // strstr return the seek position of the found substring
        char *p = strstr(line_read, STRING);
        char *q = strstr(line_read, "//");
        // p is the substring, line_read is the full string
        // substring minus the full string
        // because they are addresses, they are not integer value (eg array index, etc)
        // so substring has higher addresses value than full string
        // so, minus line_read, not line_read[0]
        // line_read[0] would mean the element of array, not the address anymore
        // lnei_read by default would mean address of the start of the string
        int p_pos = p - line_read;
        int q_pos = q - line_read;
        // If posistion of substring is later than location of '//', then skip
        if(p_pos > q_pos)
            return TRUE;
    }
    return FALSE;
}
// Deprecated, use is_comment_f_advance
/*  is_comment_function
    checks if line is comment
*/
int is_comment_f(char* line_read, int* is_comment) 
{
    if(strstr(line_read, "//"))
        return TRUE;

    // This is to handle "/*"
    if(TRUE == *is_comment)
    {
        if(strstr(line_read, "*/"))
            *is_comment = FALSE;
        return TRUE;
    }
    // This is also to handle "/*""
    if(strstr(line_read, "/*"))
    {
        if(strstr(line_read, "*/"))
            return TRUE;
        *is_comment = TRUE;
        return TRUE;
    }
    return FALSE;
}

/*  is_comment_function_advance
    checks if line is comment
    this is intended for cases like
        /*  there are cases like this
            if(perform_transaction == TRUE)
            {   // diverted for transactional writes handling (manual commit)
                ret = write_file_internal();
                return ret;
            }
        */
        /*  in which will cause the log to append in this way, and build error
            if(perform_transaction == TRUE)
            CRITICAL_MLOG(write_file_internal next);
            {   // diverted for transactional writes handling (manual commit)
                ret = write_file_internal();
                return ret;
            }
        */
        // the problem is, in this is comment case, have to update prev_seek.
        // So, my solution is, if the first 2 char is not start wtih "//" or "/*"
        // Then, update the previous seek, then skip
//*/
int is_comment_f_advance(char* line_read, int* is_comment, int* prev_seek, FILE* fp) 
{
    // This checks whether there's white spaces before the comment symbol or not
    char *p = line_read;
    while(*p && isspace(*p))
    {
        p++;
    }

    // after whitespaces, check if first 2 char is "//"
    if(0 == strncmp(p, "//", 2))
    {
        // Record and store into "previous" variable
        *prev_seek = ftell(fp);
        return TRUE;
    }

    // This is to handle "/*"
    if(TRUE == *is_comment)
    {
        if(strstr(p, "*/"))
        {
            *is_comment = FALSE;
        }
        // Record and store into "previous" variable
        *prev_seek = ftell(fp);
        return TRUE;
    }
    // This is also to handle "/*"
    if(0 == strncmp(p, "/*", 2))
    {
        if(strstr(p, "*/"))
        {
            // Record and store into "previous" variable
            *prev_seek = ftell(fp);
            return TRUE;
        }
        *is_comment = TRUE;
        // Record and store into "previous" variable
        *prev_seek = ftell(fp);
        return TRUE;
    }
    return FALSE;
}

// Return Value:
// cd ./R0082/trbo; git check-ignore -v ltd_apps 
// ^ not ignored path, ret result >0
// cd ./R0082/trbo/gemstones/projects_output_folder; git check-ignore -v rajang_fw_OUT 
// ^ ignored path, ret result == 0
int check_git_ignore(struct dirent* ep, char* path)
{
    char* cmd = NULL;

    cmd = malloc(strlen("cd ") + strlen(path) + strlen("; ") + strlen(GIT_IGNORE_CMD) + strlen(ep->d_name) + 1);
    if(NULL == cmd)
    {
        printf("%s:%d malloc failed. Terminating program.\n", __FUNCTION__, __LINE__);
        exit(0);
    }
    snprintf(cmd, strlen("cd ") + strlen(path) + strlen("; ") + strlen(GIT_IGNORE_CMD) + strlen(ep->d_name) + 1, "%s%s%s%s%s", "cd ", path, "; ", GIT_IGNORE_CMD, ep->d_name);

    return system(cmd);
}


int check_file(struct dirent* ep, char* path)
{
    char* filetype = NULL;
    glob_t gstruct;
    int ret = -1;
    char **file_extension_found;
    char glob_pattern[256] = {'\0'};
    int len = 0;
    int found = FALSE;

    // Make sure path is not full path with file extension
    // Cos you cannot 'cd' into file extension.
    // e.g: path = ./a              (can)
    //      path = ./a/debug.log    (cannot)
    if(0 == check_git_ignore(ep, path))
        return SKIP;

    // locate substring - locate the file extension
    filetype = strstr(ep->d_name, ".");

    // No file extension, just skip
    if(NULL == filetype)
        return SKIP;
    
    for(int i=0; i<ARR_SIZE(filetype_to_work); i++)
    {
        // Cautions: Cannot do like this
        /*
            // If the extension is NOT in the whitelist
            if(0 != strcmp(filetype, filetype_to_work[i]))
                return SKIP;

            this means that it only check the 1st elment of array
            If not match, return SKIP
            not checking on the 2nd element
            That is, only .c file will be written
        */
        // If the extension is in the whitelist
        if(0 == strcmp(filetype, filetype_to_work[i]))
            found = TRUE;
    }

    if(TRUE == found)
        return PROCEED;

    return SKIP;


// GLOB METHOD, WIP
//     // locate substring - locate the file extension
//     filetype = strstr(ep->d_name, ".");
//     if(filetype)
//     {
// #ifdef DEBUG
//         // puts(filetype);
// #endif

//         // 0 == Match
//         // For glob, you have to use full path, 
//         // else, it will only search from where this current file is located
//         // If want to match multiple pattern, do like linux bash terminal
//         // string = /path/*[.c|.h|.cpp];
//         // glob(string, param2, param3, param4);
//         len = strlen(path) + strlen("/*") + strlen(FILE_EXTENSION) + 1;
//         snprintf(glob_pattern, len, "%s%s%s", path, "/*", FILE_EXTENSION);
//         puts(glob_pattern);
//         len = 0;
// #ifdef DEBUG
//         puts(glob_pattern); 
// #endif
//         ret = glob(glob_pattern, GLOB_ERR , NULL, &gstruct);
//         if(0 == ret)
//         {
//             puts("MEEEEEEEEEEEEEEEEEEEEEEEEE");
//             // This is just to print out gstruct.gl_pathv value
//             // Example output: Found: ./path/to/file.c
//             // file_extension_found = gstruct.gl_pathv;
//             // while(*file_extension_found)
//             // {
//             //     printf("Found: %s\n",*file_extension_found);
//             //     file_extension_found++;
//             // }

//             // use "path", not "file_to_open"
//             // file_to_open contains full path ending wtih file extension
//             // you cannot 'cd' into file extension.
//             // e.g: path = ./a
//             //      file_to_open = ./a/debug.log
//             if(0 == check_git_ignore(ep, path))
//                 return SKIP;
//             return PROCEED;
//         }
//     }

}

DIR* open_dir(DIR* dp, char* path)
{
    dp = opendir (path);
    if (dp != NULL)
        return dp;
    perror ("Couldn't open the directory");
    printf ("%s:%s:%d path = %s, err = %d\n", __FILE__, __FUNCTION__, __LINE__, path, errno);
    return NULL;
}

int check_dir(struct dirent* ep, char* path)
{
    for(int i=0; i<ARR_SIZE(exclude_dir_and_files); i++)
    {
        if( // here will skip files as defined in exclude_dir_and_files
            (0 == strncmp(ep->d_name, exclude_dir_and_files[i], strlen(exclude_dir_and_files[i]))) &&
            (strlen(ep->d_name) == strlen(exclude_dir_and_files[i])) // this is to ensure do not skip for d_name that contains the word. Unless len are equally matched.
          )
            return SKIP;
    }
    
    // this one very hard to do
    // current problem: it scan R0041/trbo
    // if non dir matches, it basically treat program finsihed.
    // for(int i=0; i<ARR_SIZE(include_dir); i++)
    // {
    //     if( // here will check if dir is in the include_dir
    //         (0 == strncmp(ep->d_name, include_dir[i], strlen(include_dir[i]))) &&
    //         (strlen(ep->d_name) == strlen(include_dir[i])) // this is to ensure do not skip for d_name that contains the word. Unless len are equally matched.
    //       )
    //       {
    //         puts("AHaaaaaH");
    //         break;
    //       }
    //     puts(ep->d_name);
    //     puts("AHH");
    //     return SUCCESS;
    // }


    //https://sites.uclouvain.be/SystInfo/usr/include/dirent.h.html
    /* File types for `d_type'. 
        DT_UNKNOWN  = 0      The type is unknown. Only some filesystems have full support to return the type of the file, others might always return this value.
        DT_FIFO     = 1      A named pipe, or FIFO. See FIFO Special Files.
        DT_CHR      = 2      A character device.
        DT_DIR      = 4      A directory.
        DT_BLK      = 6      A block device.
        DT_REG      = 8      A regular file.
        DT_LNK      = 10     A symbolic link.
        DT_SOCK     = 12     A local-domain socket.
        DT_WHT      = 14
    */

    // is regular file
    if(8 == ep->d_type)
        return IS_FILE;

    // is a dir
    else if(4 == ep->d_type)
        return IS_DIR;

    // Unknown, just skip
    return SKIP;
}


int write_file_short( 
                FILE* fp,
                char* file_to_open,
                char* temp,
                char* buffer,
                char* str_to_write,
                char* line_read,
                int* prev_seek,
                unsigned int* old_file_size,
                unsigned int* new_file_size,
                int* bytes_written,
                const char* MACRO
                )
{
    int cur_seek = 0;
    int read_size = 0;

    // record the cur position
    cur_seek        = ftell(fp); 

    // Note: prev_seek, not cur_seek
    *new_file_size  = *old_file_size - *prev_seek + strlen(MACRO);
    read_size       = *old_file_size - *prev_seek;
    temp            = realloc(buffer, read_size + 1); // You can realloc without malloc first
    if(NULL == temp)
    {
        printf("%s:%d realloc failed. Terminating program.\n", __FUNCTION__, __LINE__);
        exit(0);
    }
    else
        buffer = temp;
    fseek(fp, *prev_seek, SEEK_SET);      // set current seek to prev_seek
    fread(buffer, read_size, 1, fp);    // read the whole content start from prev_seek
    fseek(fp, *prev_seek, SEEK_SET);      // after read, set seek back to prev position
    temp            = realloc(str_to_write, *new_file_size + 1);
    if(NULL == temp)
    {
        printf("%s:%d realloc failed. Terminating program.\n", __FUNCTION__, __LINE__);
        exit(0);
    }
    else
        str_to_write = temp;
    snprintf(str_to_write, *new_file_size + 1, "%s%s", MACRO, buffer);

    *bytes_written   = fwrite(str_to_write , 1, *new_file_size, fp);
    if(*bytes_written != *new_file_size)
    {
        printf("%s:%d Write failed. Terminate program.\n", __FUNCTION__, __LINE__);
        exit(0);
    }
    fseek(fp, cur_seek + strlen(MACRO), SEEK_SET);   // after write, set seek back to prev position + pos of log written
    
    *old_file_size   += strlen(MACRO); // update file size
    
    // reset pointer
    buffer          = NULL; // You have to free for above & below realloc. Realloc doesn't clear pointer content. And after fread, fread doesn't clear content too, only replace. If read value samller than pointer's content, the old content will still be in pointer there.
    str_to_write    = NULL;

    return SUCCESS;
}



// Initialize regex variable
void init_regex()
{
    int ret_regex = 0;

/*---------------------------------MATCH--------------------------------------------------------*/

    ret_regex = regcomp( &reegex_match, POSIX_regex_match[0], REGEX_FLAG);
    if(ret_regex != 0)
    {
        printf("%s:%d Regex Failed. Terminating Program\n", __FUNCTION__, __LINE__);
        exit(0);
    }
    ret_regex = regcomp( &reegex_match1, POSIX_regex_match[1], REGEX_FLAG);
    if(ret_regex != 0)
    {
        printf("%s:%d Regex Failed. Terminating Program\n", __FUNCTION__, __LINE__);
        exit(0);
    }
    ret_regex = regcomp( &reegex_match2, POSIX_regex_match[2], REGEX_FLAG);
    if(ret_regex != 0)
    {
        printf("%s:%d Regex Failed. Terminating Program\n", __FUNCTION__, __LINE__);
        exit(0);
    }
    ret_regex = regcomp( &reegex_match3, POSIX_regex_match[3], REGEX_FLAG);
    if(ret_regex != 0)
    {
        printf("%s:%d Regex Failed. Terminating Program\n", __FUNCTION__, __LINE__);
        exit(0);
    }

/*---------------------------------NO MATCH--------------------------------------------------------*/

    ret_regex = regcomp( &reegex_no_match, POSIX_regex_no_match[0], REGEX_FLAG);
    if(ret_regex != 0)
    {
        printf("%s:%d Regex Failed. Terminating Program\n", __FUNCTION__, __LINE__);
        exit(0);
    }
    ret_regex = regcomp( &reegex_no_match1, POSIX_regex_no_match[1], REGEX_FLAG);
    if(ret_regex != 0)
    {
        printf("%s:%d Regex Failed. Terminating Program\n", __FUNCTION__, __LINE__);
        exit(0);
    }
    ret_regex = regcomp( &reegex_no_match2, POSIX_regex_no_match[2], REGEX_FLAG);
    if(ret_regex != 0)
    {
        printf("%s:%d Regex Failed. Terminating Program\n", __FUNCTION__, __LINE__);
        exit(0);
    }
    ret_regex = regcomp( &reegex_no_match3, POSIX_regex_no_match[3], REGEX_FLAG);
    if(ret_regex != 0)
    {
        printf("%s:%d Regex Failed. Terminating Program\n", __FUNCTION__, __LINE__);
        exit(0);
    }
    ret_regex = regcomp( &reegex_no_match4, POSIX_regex_no_match[4], REGEX_FLAG);
    if(ret_regex != 0)
    {
        printf("%s:%d Regex Failed. Terminating Program\n", __FUNCTION__, __LINE__);
        exit(0);
    }
    ret_regex = regcomp( &reegex_no_match5, POSIX_regex_no_match[5], REGEX_FLAG);
    if(ret_regex != 0)
    {
        printf("%s:%d Regex Failed. Terminating Program\n", __FUNCTION__, __LINE__);
        exit(0);
    }
    ret_regex = regcomp( &reegex_no_match6, POSIX_regex_no_match[6], REGEX_FLAG);
    if(ret_regex != 0)
    {
        printf("%s:%d Regex Failed. Terminating Program\n", __FUNCTION__, __LINE__);
        exit(0);
    }
    ret_regex = regcomp( &reegex_no_match7, POSIX_regex_no_match[7], REGEX_FLAG);
    if(ret_regex != 0)
    {
        printf("%s:%d Regex Failed. Terminating Program\n", __FUNCTION__, __LINE__);
        exit(0);
    }
    ret_regex = regcomp( &reegex_no_match8, POSIX_regex_no_match[8], REGEX_FLAG);
    if(ret_regex != 0)
    {
        printf("%s:%d Regex Failed. Terminating Program\n", __FUNCTION__, __LINE__);
        exit(0);
    }
    ret_regex = regcomp( &reegex_no_match9, POSIX_regex_no_match[9], REGEX_FLAG);
    if(ret_regex != 0)
    {
        printf("%s:%d Regex Failed. Terminating Program\n", __FUNCTION__, __LINE__);
        exit(0);
    }
    ret_regex = regcomp( &reegex_no_match10, POSIX_regex_no_match[10], REGEX_FLAG);
    if(ret_regex != 0)
    {
        printf("%s:%d Regex Failed. Terminating Program\n", __FUNCTION__, __LINE__);
        exit(0);
    }
    ret_regex = regcomp( &reegex_no_match11, POSIX_regex_no_match[11], REGEX_FLAG);
    if(ret_regex != 0)
    {
        printf("%s:%d Regex Failed. Terminating Program\n", __FUNCTION__, __LINE__);
        exit(0);
    }
    ret_regex = regcomp( &reegex_no_match12, POSIX_regex_no_match[12], REGEX_FLAG);
    if(ret_regex != 0)
    {
        printf("%s:%d Regex Failed. Terminating Program\n", __FUNCTION__, __LINE__);
        exit(0);
    }
    ret_regex = regcomp( &reegex_no_match13, POSIX_regex_no_match[13], REGEX_FLAG);
    if(ret_regex != 0)
    {
        printf("%s:%d Regex Failed. Terminating Program\n", __FUNCTION__, __LINE__);
        exit(0);
    }
    ret_regex = regcomp( &reegex_no_match14, POSIX_regex_no_match[14], REGEX_FLAG);
    if(ret_regex != 0)
    {
        printf("%s:%d Regex Failed. Terminating Program\n", __FUNCTION__, __LINE__);
        exit(0);
    }
    ret_regex = regcomp( &reegex_no_match15, POSIX_regex_no_match[15], REGEX_FLAG);
    if(ret_regex != 0)
    {
        printf("%s:%d Regex Failed. Terminating Program\n", __FUNCTION__, __LINE__);
        exit(0);
    }
    ret_regex = regcomp( &reegex_no_match16, POSIX_regex_no_match[16], REGEX_FLAG);
    if(ret_regex != 0)
    {
        printf("%s:%d Regex Failed. Terminating Program\n", __FUNCTION__, __LINE__);
        exit(0);
    }
    ret_regex = regcomp( &reegex_no_match17, POSIX_regex_no_match[17], REGEX_FLAG);
    if(ret_regex != 0)
    {
        printf("%s:%d Regex Failed. Terminating Program\n", __FUNCTION__, __LINE__);
        exit(0);
    }
    ret_regex = regcomp( &reegex_no_match18, POSIX_regex_no_match[18], REGEX_FLAG);
    if(ret_regex != 0)
    {
        printf("%s:%d Regex Failed. Terminating Program\n", __FUNCTION__, __LINE__);
        exit(0);
    }
}