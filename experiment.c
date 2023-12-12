#include <stdio.h>

// #define NUM 3

/****
 * Behaviour
 * NUM will be according to the '-DNUM=value' pass in
 * 
 * If you try to redefine it
 * It will prompt warning redefined
 * But program still able to run
 * And the value will use the one defined in here,
 * rather than the value passed in from makefile
 * 
 * If you pass in '-DNUM' like that
 * That is, no value
 * Then, it has default value of 1 (TRUE)
*/

int main()
{
    printf("IT'S MEEEE %d\n", NUM);

    #if NUM==3
        printf("YOOOOOO\n");
    #endif
}