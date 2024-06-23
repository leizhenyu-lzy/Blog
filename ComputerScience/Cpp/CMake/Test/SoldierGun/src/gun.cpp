#include <iostream>
#include "gun.h"

Gun::Gun(std::string type)
{
    this->type = type;
    this->bullet = 0;
}

void Gun::addBullet(int num)
{
    this->bullet += num;
}
void Gun::shoot()
{
    if (this->bullet > 0)
    {
        this->bullet--;
        std::cout << "shoot" << std::endl;
    }
    else
    {
        std::cout << "no bullet" << std::endl;
    }
}
