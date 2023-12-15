

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

#define PUT_YOUR_SEARCH_KEYWORD_HERE   "\tprintf(\"ME\");\n"
#define LOG_PUT_YOUR_SEARCH_KEYWORD_HERE   "\tprintf(\"ME\");\n"


int read_line(char* file_to_open)
{
    char line_read[MAX_READ_SIZE_PER_LINE] = {'\0'};
    unsigned int old_file_size = 0;
    FILE* fp = NULL;
    char* buffer = NULL;
    int is_comment = FALSE;
    char* temp = NULL;
    int ret = FALSE;
    int bytes_written = 0;
    char* str_to_write = NULL;
    unsigned int new_file_size = 0;
    int prev_seek = 0;

    fp = fopen(file_to_open, "r+");
    if(NULL == fp)
    {
        printf("%s:%d Open file failed: path = %s, err = %d\n", __FUNCTION__, __LINE__, file_to_open, errno);
        return FAILURE;
    }

    fseek(fp, 0, SEEK_END);     // seek end of file
    old_file_size = ftell(fp);  // get the whole file size
    fseek(fp, 0, SEEK_SET);     // set back to start of file

    // read file content line by line & write
    while(NULL != fgets(line_read, MAX_READ_SIZE_PER_LINE, fp))
    {
        // cannot check if line is comment, there are cases
        /*
            if()
            { // comments //
                vr_capture_semevent
            }
        */
        // resulting
        /*
            if()
            CRITICAL_MLOG(..)
            { // comments //
                vr_capture_semevent
            }
        */

        // if(strstr(line_read, "//"))
        //     continue;

        // // This is to handle "/*"
        // if(TRUE == is_comment)
        // {
        //     if(strstr(line_read, "*/"))
        //         is_comment = FALSE;
        //     continue;
        // }
        // // This is also to handle "/*""
        // if(strstr(line_read, "/*"))
        // {
        //     if(strstr(line_read, "*/"))
        //         continue;
        //     is_comment = TRUE;
        //     continue;
        // }

        if( strstr(line_read, "PUT_YOUR_SEARCH_KEYWORD_HERE"))
        {
            ret = write_file_short(fp, file_to_open, temp, buffer, str_to_write, line_read, &prev_seek, &old_file_size, &new_file_size, &bytes_written, LOG_PUT_YOUR_SEARCH_KEYWORD_HERE);
            if(SUCCESS != ret)
            {
                printf("%s:%d write file failed. Terminating program.\n", __FUNCTION__, __LINE__);
                exit(0);
            }
        }

        // Record and store into "previous" variable
        prev_seek = ftell(fp);

    } // while

    // If has log written in file, then write the library
    // Dont check if lib has included it or not, just include. Becos there are files that #ifdef UNIT_TEST n only then it includes <stdio.h>
    if(SUCCESS == ret)
    {
        new_file_size   = old_file_size + strlen(LIB_TO_WRITE);

        fseek(fp, 0, SEEK_SET);             // set to start of file
        temp            = realloc(buffer, old_file_size + 1); // old_file_size has been updated to size that written log from above
        if(NULL == temp)
        {
            printf("%s:%d realloc failed. Terminating program.\n", __FUNCTION__, __LINE__);
            exit(0);
        }
        else
            buffer = temp;
        fread(buffer, old_file_size, 1, fp);    // read the whole content from start
        fseek(fp, 0, SEEK_SET);             // after read, set to start of file again
        temp            = realloc(str_to_write, new_file_size + 1);
        if(NULL == temp)
        {
            printf("%s:%d realloc failed. Terminating program.\n", __FUNCTION__, __LINE__);
            exit(0);
        }
        else
            str_to_write = temp;
        snprintf(str_to_write, new_file_size + 1, "%s%s", LIB_TO_WRITE, buffer);
#ifdef DEBUG
        // puts(str_to_write);
        // puts("\nBREAKS\nBREAKS\n");
        // exit(0);
#else
        bytes_written   = fwrite(str_to_write , 1, new_file_size, fp);
        if(bytes_written != new_file_size)
        {
            printf("%s:%d Write failed. Terminate program.\n", __FUNCTION__, __LINE__);
            exit(0);
        }
#endif
        // fseek(fp, 0, SEEK_END); // not needed, after write, means at the end of file ady. Since u're writting whole content
    }

    // Output what file has been written
    // Can park together with 'if' from above, but this is purely readability and cosmetics
    if(SUCCESS == ret)
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
    return SUCCESS;
}


int main (int argc, char* argv[])
{
    DIR* dp = NULL; // maybe is Directory Pointer, to open directory
    struct dirent* ep; // maybe is Directory Entry Pointer, to store detail of directory
    char* path = NULL; // the path to repo/dir that contains source file to append logs
    char* file_to_open = NULL;
    char** stack = NULL;
    char** temp_stack = NULL;
    char* next_path = NULL;
    char* current_dir = NULL;
    char* base_path = NULL;
    char* temp = NULL;
    int length = 0;
    int check_file_ret = INVALID;
    int check_dir_ret = INVALID;

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
        printf("%s:%d Terminate\n", __FUNCTION__, __LINE__);
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
            printf("%s:%d Terminate\n", __FUNCTION__, __LINE__);
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
                    printf("%s:%d Terminate\n", __FUNCTION__, __LINE__);
                    exit(0);
                }
                snprintf(file_to_open, length + 1, "%s%s%s", base_path, "/", ep->d_name);

                read_line(file_to_open);
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
                    printf("%s:%d Terminate\n", __FUNCTION__, __LINE__);
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
                        printf("%s:%d Terminate\n", __FUNCTION__, __LINE__);
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