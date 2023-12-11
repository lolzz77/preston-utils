#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <dirent.h>
#include <errno.h>

#define SUCCESS 1
#define FAILURE -1
#define TRUE    1
#define FALSE   0

#define CONSTRUCT_PATH_LEN(a, b, c)     (strlen(a) + strlen(b) + strlen(c))
#define TRBO_PATH                       "/trbo"
#define CUR_PATH                        "./"
#define CMD                             "git reset --hard HEAD"

DIR* open_dir(DIR* dp, char* path)
{
    dp = opendir (path);
    if (dp != NULL)
        return dp;
    perror ("Couldn't open the directory");
    printf ("%s:%d path = %s, err = %d\n", __FUNCTION__, __LINE__, path, errno);
    return NULL;
}

int check_dir(struct dirent* ep, char* path)
{
    char* next_path = NULL;
    DIR* next_dp = NULL;
    struct dirent* next_ep = NULL;
    char* buffer = NULL;
    int len = 0;
#ifdef DEBUG
    puts(ep->d_name);
#endif
    if(0 == strncmp(ep->d_name, ".git", strlen(".git")))
    {
        len = strlen("cd ") + strlen(path) + strlen("; ") + strlen(CMD);
        buffer = malloc(len + 1);
        snprintf(buffer, len + 1, "%s%s%s%s", "cd ", path, "; ", CMD);
#ifdef DEBUG
        puts(buffer);
#else
        system(buffer);
#endif
    }

    // skip those files that begin with '.' after checking it's not .git
    if(0 == strncmp(ep->d_name, ".", 1))
        return SUCCESS;

    // if is a dir
    else if(4 == ep->d_type)
    {
        next_path = malloc(CONSTRUCT_PATH_LEN(path, "/", ep->d_name) + 1);
        if(NULL == next_path)
        {
            printf("%s:%d Next_path malloc failed\n", __FUNCTION__, __LINE__);
            return FAILURE;
        }
        snprintf(next_path, CONSTRUCT_PATH_LEN(path, "/", ep->d_name) + 1, "%s%s%s", path, "/", ep->d_name);
#ifdef DEBUG
        // puts(next_path);
#endif
        next_dp = open_dir(next_dp, next_path);
        if(NULL == next_dp)
        {
            printf("%s:%d Open dir failed. Terminate program\n", __FUNCTION__, __LINE__);
            exit(0);
        }
        while ((next_ep = readdir (next_dp)) != NULL)
        {
            if(SUCCESS != check_dir(next_ep, next_path))
            {
                printf("%s:%d check dir fails. Terminate program\n", __FUNCTION__, __LINE__);
                exit(0);
            }
        }
    }

    // cleanup
    if(NULL != buffer)
    {
        free(buffer);
        buffer = NULL;
    }
    if(NULL != next_ep)
    {
        free(next_ep);
        next_ep = NULL;
    }
    if(NULL != next_path)
    {
        free(next_path);
        next_path = NULL;
    }
    if(NULL != next_dp)
    {
        (void) closedir (next_dp);
        next_dp = NULL;
    }
    
    return SUCCESS;
}

int main (int argc, char* argv[])
{
    if(argc != 2)
    {
        printf("Please enter repo dir name\n");
        return 0;
    }

    printf("Begin operation... please wait...\n");

    DIR* dp = NULL; // maybe is Directory Pointer
    struct dirent* ep; // maybe is Directory Entry Pointer
    char* path = NULL;

    path = malloc(CONSTRUCT_PATH_LEN(CUR_PATH, argv[1], TRBO_PATH) + 1);
    snprintf(path, CONSTRUCT_PATH_LEN(CUR_PATH, argv[1], TRBO_PATH) + 1, "%s%s%s", CUR_PATH, argv[1], TRBO_PATH);
#ifdef DEBUG
    // puts(path);
#endif

    dp = open_dir(dp, path);
    if(NULL == dp)
    {
        printf("%s:%d open dir fails. Terminate program\n", __FUNCTION__, __LINE__);
        exit(0);
    }
    while ((ep = readdir (dp)) != NULL)
    {
        if(SUCCESS != check_dir(ep, path))
        {
            printf("%s:%d check dir fails. Terminate program\n", __FUNCTION__, __LINE__);
            exit(0);
        }
    }

    // cleanup
    if(NULL != ep)
    {
        free(ep);
        ep = NULL;
    }
    if(NULL != dp)
    {
        (void) closedir (dp);
        dp = NULL;
    }
    if(NULL != path)
    {
        free(path);
        path = NULL;
    }

    printf("Operation finished\n");

    return 0;
}