#include <iostream>

using namespace std;

int main(int argc, char **argv)
{
    #ifdef DEBUG
        cout << "Debug mode" << endl;
    #endif

    cout << "Hello, world!" << endl;
    return 0;
}


