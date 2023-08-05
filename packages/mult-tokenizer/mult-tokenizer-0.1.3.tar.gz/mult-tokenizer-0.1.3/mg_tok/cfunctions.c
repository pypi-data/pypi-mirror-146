
#include "cfunctions.h"

int a = 5;
double b = 5.12345;
char c = 'X';

int func_ret_int(int val) {
    printf("get func_ret_int: %d\n", val);
    return val;
}

double func_ret_double(double val) {
    printf("get func_ret_double_c: %f\n", val);
    return val;
}

char * func_ret_str(char *val) {
    printf("get func_ret_str: %s\n", val);
    return val;
}

char
func_many_args(int val1, double val2, char val3, short val4) {
    printf("get func_many_args: int - %d, double - %f, char - %c, short - %d\n", val1, val2, val3, val4);
    return val3;
}
