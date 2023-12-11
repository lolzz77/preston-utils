/*
    TODO
    1. why CommonHostInitializer.cpp didn't get written
    2. false append in hush.c
    3. try put fprintf in audio volumn adjustment there and see if will print on console
*/

/*  HOW-TO-RUN
    1. fix bugs that you have in your repo first
    2. commit/save your whole repo
    3. put in /data/<coreID>
    4. open linux terminal, run
    5.  gcc -g -o [file output name] [this file name.c]
        OR if you want trigger #ifdef DEBUG
        gcc -g -o [file output name] [this file name.c] -DDEBUG
    6. ./[file output name] [repo name]/trbo
*/

/*  INFO
    1. opendir
    To open dir, dont need '/' at the end
    passed in value: "./R0082/trbo"

    2.      // dont think this one is needed,
            // realloc resize the memory pointed by buffer
            // then it assign to temp
            // now temp points to buffer's block memory + new size u just specified (maybe this is the logic)
            // so you just assign buffer = temp and can already.

            // and one more thing, u shoulnd't free it before realloc
            // realloc 1st param takes the buffer pointer. 

            // and also, in stackoverflow, https://stackoverflow.com/questions/1986538/how-to-handle-realloc-when-it-fails-due-to-memory
            // if realloc fails, temp will be invalid,
            // however, buffer is still valid

            // and also, i dont think u need to declare temp1, temp2, temp3 variable if u happen to realloc multiple times
            // because once u assign buffer = temp
            // u can let go of temp already
            // and if u realloc to temp again
            // rmb realloc 1st param takes the pointer to the prev pointer that assigned by malloc calloc realloc?
            // the 1st param is buffer pointer, not temp pointer
            // so if u happen to realloc to temp again, u dont need to free(temp) before the realloc
            if(NULL != buffer)
            {
                free(buffer);
                buffer = NULL;
            }
            temp1           = realloc(buffer, read_size + 1); // You can realloc without malloc first
            if(NULL == temp1)
            {
                printf("%s:%s:%d realloc failed. Terminating program.\n", __FILE__, __FUNCTION__, __LINE__);
                exit(0);
            }
            else
            {
                buffer = temp1;
                // free(temp); // you should not free, next_path is pointing to temp addr now, if u free temp, next_path will be affected
            }

    3. The reasonw why u get double free corruption
    It is not related to recursive function calls
    https://stackoverflow.com/questions/52563137/why-am-i-getting-double-free-or-corruption-with-the-following-code

    if(NULL != buffer)
    {
        free(buffer); // dk why this cause double free error
        buffer = NULL;
    }
    if(NULL != str_to_write)
    {
        free(str_to_write);
        str_to_write = NULL;
    }
    if(NULL != temp)
    {
        // at here, temp is either pointing to buffer or str_to_write
        // freeing both of them would also free 'temp'
        // free(temp); // this will cause double free corruption. 
        temp = NULL;
    }
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <dirent.h>
#include <fcntl.h>
#include <errno.h>
#include <limits.h>
#include <regex.h>

#include "include.h"

// #define LOG_TO_WRITE                    "\tfprintf(stdout, \"%s\\n%s:%d\\n\\n\", __FILE__, __FILE__, __FUNCTION__, __LINE__);\n"

// #define LOG_TO_WRITE                    "\tprintf(\"MEE %s:%s:%d\\r\\n\", __FILE__, __FUNCTION__, __LINE__);\n"

#define LOG_TO_WRITE                    "\tprintf(\"MEE %s\\r\\n\", __FILE__);\n" \
                                        "\tprintf(\" " COLOR_YELLOW " \\t %s:%d " COLOR_RESET " \\r\\n\", __FUNCTION__, __LINE__);\n" \
                                        "\tprintf(\"\\t Thread ID: %lu\\r\\n\\n\", pthread_self());\n" \


int write_file_long(char* file_to_open, const char* MACRO)
{
    unsigned int old_file_size = 0;
    unsigned int new_file_size = 0;
    char line_read[MAX_READ_SIZE_PER_LINE] = {'\0'};
    int open_bracket = 0;
    int close_bracket = 0;
    int read_size = 0;
    int cur_seek = 0;
    int bytes_written = 0;
    int is_func = FALSE;
    FILE* fp = NULL;
    char* str_to_write = NULL;
    char* buffer = NULL;
    int include_lib = FALSE;
    int is_comment = FALSE;
    int multiline = FALSE;
    char* temp = NULL;
    int is_written = FALSE;

    fp = fopen(file_to_open, "r+");
    if(NULL == fp)
    {
        printf("%s:%s:%d path = %s, err = %d\n", __FILE__, __FUNCTION__, __LINE__, file_to_open, errno);
        printf("%s:%s:%d Terminate\n", __FILE__, __FUNCTION__, __LINE__);
        exit(0);
    }

    fseek(fp, 0, SEEK_END);     // seek end of file
    old_file_size = ftell(fp);  // get the whole file size
    fseek(fp, 0, SEEK_SET);     // set back to start of file

    // read file content line by line & write
    while(NULL != fgets(line_read, MAX_READ_SIZE_PER_LINE, fp))
    {
        if(TRUE == is_comment_f(line_read, &is_comment))
            continue;

        if
        ( 
            (no_match(line_read, file_to_open)) &&
            (match(line_read) || (TRUE == is_func))
        )
        {
            // skip these, it means they are not function definition
            // "[,]", // No, function param have them
            if  
            ( 
                strstr(line_read, "}") || // might have a change where compelte function were written in 1 line, but rare chance
                strstr(line_read, ";") ||
                strstr(line_read, "=")
            )
                continue;
                
            else if(NULL == strstr(line_read, "{"))
            {
                is_func = TRUE;
                continue;
            }
            else
                is_func = FALSE;

            cur_seek        = ftell(fp);   // get current seek position, it will be already at the end of line_read

            // Check if next line is KEYWORD HERE
            // search for "Check if next line is" in the file under the folder name 'myNote'
            // read the next line
            fgets(line_read, MAX_READ_SIZE_PER_LINE, fp);
            if(strstr(line_read, "KEYWORD HERE"))
                // set the seek to the next line
                cur_seek        = ftell(fp);
            else
                // set the seek back to prev line
                fseek(fp, cur_seek, SEEK_SET);

            new_file_size   = old_file_size - cur_seek + strlen(MACRO);
            read_size       = old_file_size - cur_seek;
            temp            = realloc(buffer, read_size + 1); // You can realloc without malloc first

            // This is to handle check if realloc has failed
            if(NULL == temp)
            {
                printf("%s:%s:%d Terminate\n", __FILE__, __FUNCTION__, __LINE__);
                exit(0);
            }
            else
                buffer = temp;
                
            fread(buffer, read_size, 1, fp);    // read the whole content start from cur_seek
            fseek(fp, cur_seek, SEEK_SET);      // after read, set seek back to prev position
            temp            = realloc(str_to_write, new_file_size + 1);

            // This is to handle check if realloc is fail
            if(NULL == temp)
            {
                printf("%s:%s:%d Terminate\n", __FILE__, __FUNCTION__, __LINE__);
                exit(0);
            }
            else
                str_to_write = temp;

            snprintf(str_to_write, new_file_size + 1, "%s%s", MACRO, buffer);

            // puts(line_read);

            bytes_written   = fwrite(str_to_write , 1, new_file_size, fp);
            if(bytes_written != new_file_size)
            {
                printf("%s:%s:%d Terminate\n", __FILE__, __FUNCTION__, __LINE__);
                exit(0);
            }

            // To output log that this file is written
            is_written = TRUE;


            fseek(fp, cur_seek + strlen(MACRO), SEEK_SET);   // after write, set seek back to prev position + pos of log written
            old_file_size   += strlen(MACRO); // update file size
// #endif
            // If there's log written, then include the lib
            // Dont check if file has included it or not, just include. Becos there are files that #ifdef UNIT_TEST n only then it includes <stdio.h>
            include_lib = TRUE;

            // reset pointer
            buffer          = NULL; // You have to free for above & below realloc. Realloc doesn't clear pointer content. And after fread, fread doesn't clear content too, only replace. If read value samller than pointer's content, the old content will still be in pointer there.
            str_to_write    = NULL;
            multiline       = FALSE;
            // memset(line_read, 0, sizeof(line_read)); // You dont need this, every fgets will reset the line_read, and this will interfere with your blank line checking below
        } // if
    } // while
    
    if(TRUE == include_lib)
    {
        new_file_size   = old_file_size + strlen(LIB_TO_WRITE);

        fseek(fp, 0, SEEK_SET);             // set to start of file
        temp            = realloc(buffer, old_file_size + 1); // old_file_size has been updated to size that written log from above

        // This is to handle check if realloc is fail
        if(NULL == temp)
        {
            printf("%s:%s:%d Terminate\n", __FILE__, __FUNCTION__, __LINE__);
            exit(0);
        }
        else
            buffer = temp;

        fread(buffer, old_file_size, 1, fp);    // read the whole content from start
        fseek(fp, 0, SEEK_SET);             // after read, set to start of file again
        temp            = realloc(str_to_write, new_file_size + 1);

        // This is to handle check if realloc is fail
        if(NULL == temp)
        {
            printf("%s:%s:%d Terminate\n", __FILE__, __FUNCTION__, __LINE__);
            exit(0);
        }
        else
            str_to_write = temp;

        snprintf(str_to_write, new_file_size + 1, "%s%s", LIB_TO_WRITE, buffer);

        bytes_written   = fwrite(str_to_write , 1, new_file_size, fp);
        if(bytes_written != new_file_size)
        {
            printf("%s:%s:%d Terminate\n", __FILE__, __FUNCTION__, __LINE__);
            exit(0);
        }
        // include_lib = FALSE; // not needed, only need when this is in a loop function
        // fseek(fp, 0, SEEK_END); // not needed, after write, means at the end of file ady. Since u're writting whole content
    }

    if(TRUE == is_written)
    {
        printf("Writting ");
        puts(file_to_open);
    }

cleanup:
    if(NULL != fp)
    {
        fclose(fp);
        fp = NULL;
    }
    if(NULL != buffer)
    {
        free(buffer); // dk why this cause double free error
        buffer = NULL;
    }
    if(NULL != str_to_write)
    {
        free(str_to_write);
        str_to_write = NULL;
    }
    if(NULL != temp)
    {
        // free(temp); // already freed from either buffer or str_to_write
        temp = NULL;
    }
}


int main (int argc, char* argv[])
{
    DIR* dp = NULL; // maybe is Directory Pointer, to open directory
    struct dirent* ep; // maybe is Directory Entry Pointer, to store detail of directory
    char* path = NULL; // the path to repo/dir that contains source file to append logs
    int check_file_ret = INVALID;
    int check_dir_ret = INVALID;
    char* file_to_open = NULL;
    char** stack = NULL;
    char** temp_stack = NULL;
    char* next_path = NULL;
    char* current_dir = NULL;
    char* base_path = NULL;
    char* temp = NULL;
    int length = 0;

    stack = malloc(sizeof(char *));

    if(argc != 2)
    {
        printf("Please enter repo dir name, with /trbo at the end.\n");
        return 0;
    }

    printf("Begin operation...\n");


    path = malloc(CONSTRUCT_PATH_LEN(CURRENT_PATH, argv[1], "") + 1);
    if(NULL == path)
    {
        printf("%s:%s:%d Terminate\n", __FILE__, __FUNCTION__, __LINE__);
        exit(0);
    }
    snprintf(path, CONSTRUCT_PATH_LEN(CURRENT_PATH, argv[1], "") + 1, "%s%s", CURRENT_PATH, argv[1]);

    init_regex();

    // Push string into stack
    // Initially, stack_top = 0
    // stack[stack_top++] means stack[0]
    // Then, increase stack_top by 1
    stack[stack_top++] = strdup(path);

    // No need anymore, set to point to NULL
    free(path);
    path = NULL;
    
    // Begin traversing directory
    while (stack_top > 0)
    {
        // Get the latest directory from stack
        // Pop the stack. In actuality, when you pop a stack, it just take the toppest index
        // The value is still in the stack. That's how it works
        // Later if you push a new value to stack, it will overwrite the value on that index
        current_dir = stack[--stack_top];

        // Get the base path
        // Let's say A dir has 10 subdirs
        // base_path holds path until A dir only
        // So that later snprintf, it able to append all 10 subdirs to path, and store into stack
        base_path = current_dir;

        dp = open_dir(dp, current_dir);
        if(NULL == dp)
        {
            printf("%s:%s:%d Terminate\n", __FILE__, __FUNCTION__, __LINE__);
            exit(0);
        }

        // From the directory, read all dirs/files, store them into 'ep'
        while ((ep = readdir (dp)) != NULL)
        {
            check_file_ret = INVALID;
            check_dir_ret = INVALID;

            check_dir_ret = check_dir(ep, current_dir);

            if(SKIP == check_dir_ret)
                continue;
            else if(IS_FILE == check_dir_ret)
            {
                check_file_ret = check_file(ep, current_dir);

                if(SKIP == check_file_ret)
                    continue;

                // Is valid file to append log, construct the path
                length = strlen(current_dir) + strlen("/") + strlen(ep->d_name);
                file_to_open = malloc(length + 1);
                if(NULL == file_to_open)
                {
                    printf("%s:%s:%d Terminate\n", __FILE__, __FUNCTION__, __LINE__);
                    exit(0);
                }
                snprintf(file_to_open, length + 1, "%s%s%s", base_path, "/", ep->d_name);

                write_file_long(file_to_open, LOG_TO_WRITE);
            }
            else if(IS_DIR == check_dir_ret)
            {
                if(0 == check_git_ignore(ep, current_dir))
                    continue;

                // Realloc handling, it uses the next_path's allocation, and add more memory blocks
                temp = realloc(next_path, CONSTRUCT_PATH_LEN(base_path, "/", ep->d_name) + 1);

                // This is to handle check if realloc is fail
                if(NULL == temp)
                {
                    printf("%s:%s:%d Terminate\n", __FILE__, __FUNCTION__, __LINE__);
                    exit(0);
                }
                // If no fail, proceed to let next_path to point to the new realloc
                // Now both next_path & temp are pointing to the new realloc
                // Then, dont free 'temp', if you free 'temp', it will free 'next_path' as well
                // Only set 'temp' to point to NULL
                next_path = temp;
                temp = NULL;

                // Construct next path to the next subdirectory
                snprintf(next_path, CONSTRUCT_PATH_LEN(base_path, "/", ep->d_name) + 1, "%s%s%s", base_path, "/", ep->d_name);

                // Check if stack is full
                if (stack_top == stack_size) 
                {
                    // If it is, double the size
                    // This is called 'Geometric expansion'
                    // Where doubling the size, is more performance optimized just by increasing size by 1
                    // realloc isn't simple process u know...
                    stack_size *= 2;

                    temp_stack = realloc(stack, stack_size * sizeof(char *));
                    if(NULL == temp_stack)
                    {
                        printf("%s:%s:%d Terminate\n", __FILE__, __FUNCTION__, __LINE__);
                        exit(0);
                    }
                    stack = temp_stack;
                    temp_stack = NULL;
                }
                // Push new string into index.
                // It will overwrite whatever value is in the index
                // The design is that, if dir A has 10 subdirs
                // Then push all 10 subdirs into stack
                // Then will closedir on dir A
                // Then will opendir on the 10 subdirs one by one
                // This is iteration approach to open dir recursively
                stack[stack_top++] = strdup(next_path);
            }

            // cleanup / reset
            if(NULL != temp)
                free(temp);
            temp = NULL;
            if(NULL != temp_stack)
                free(temp_stack);
            temp_stack = NULL;
            if(NULL != file_to_open)
                free(file_to_open);
            file_to_open = NULL;
            if(NULL!= next_path)
                free(next_path);
            next_path = NULL;
            length = 0;

        }

        // cleanup / reset
        closedir(dp);
        dp = NULL;
        free(next_path);
        next_path = NULL;
        free(current_dir);
        current_dir = NULL;
        // free(base_path); // no need, base_path is pointing to current_dir, u ady freed current_dir
        base_path = NULL;
    }

    // cleanup
    if(NULL != ep)
        free(ep);
    ep = NULL;
    if(NULL != dp)
        (void) closedir (dp);
    dp = NULL;
    if(NULL != path)
        free(path);
    path = NULL;
    if(NULL != file_to_open)
        free(file_to_open);
    file_to_open = NULL;
    if(NULL != stack)
        free(stack);
    stack = NULL;

    printf("Operation finished\n");
    return 0;
}