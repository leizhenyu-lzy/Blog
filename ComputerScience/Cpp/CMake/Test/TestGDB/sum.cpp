#include <iostream>

using namespace std;

void hello()
{
    cout<<"Hello!"<<endl;
}

int main(int argc, char **argv)
{
    int N = 100;
    int sum = 0;
    int i = 1;

    while (i <= N)
    {
        sum = sum + i;
        i = i + 1;
    }

    cout << "sum = " << sum << endl;

    hello();

    return 0;
}



