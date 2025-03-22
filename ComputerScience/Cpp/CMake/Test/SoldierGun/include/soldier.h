#pragma once

#include <string>
#include "gun.h"

class Soldier
{
public:
    Soldier(std::string name);
    ~Soldier();
    void addGun(Gun* gun);
    void addBulletToGun(int num);
    void fire();



private:
    std::string name;
    Gun* gun;
};




