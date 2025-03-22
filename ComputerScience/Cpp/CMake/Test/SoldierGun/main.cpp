#include <iostream>
#include "gun.h"
#include "soldier.h"
#include "hellolib.h"


void test()
{
    Soldier lzy("lzy");
    lzy.addGun(new Gun("AK47"));
    // lzy.addBulletToGun(20);
    lzy.fire();
}

int main()
{
    std::cout << "Hello!" << std::endl;
    hello();
    test();
    return 0;
}