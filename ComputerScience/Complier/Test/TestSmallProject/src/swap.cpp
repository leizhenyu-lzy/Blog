#include "swap.h"

void swap(int& a, int& b)
{
    int t = a;
    a = b;
    b = t;
}