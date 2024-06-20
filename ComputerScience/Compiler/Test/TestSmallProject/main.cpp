#include <iostream>
#include "swap.h"

using namespace std;

int main()
{
    int a = 1;
    int b = 2;
    swap(a, b);
    cout << "a = " << a << endl;
    cout << "b = " << b << endl;
    return 0;
}