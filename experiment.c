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
*/

int main()
{
    printf("IT'S MEEEE %d\n", NUM);
}