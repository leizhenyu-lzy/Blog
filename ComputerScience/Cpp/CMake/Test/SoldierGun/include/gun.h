#pragma once

#include <iostream>
#include <string>


class Gun
{
private:
    /* data */
    int bullet;
    std::string type;

public:
    Gun(std::string type);

    void addBullet(int num);
    void shoot();

};



