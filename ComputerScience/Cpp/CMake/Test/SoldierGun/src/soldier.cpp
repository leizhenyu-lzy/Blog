#include <iostream>
#include "soldier.h"

Soldier::Soldier(std::string name)
{
    this->name = name;
    this->gun = NULL;
}

void Soldier::addBulletToGun(int num)
{
    this->gun->addBullet(num);
}

void Soldier::addGun(Gun* gun)
{
    this->gun = gun;
}

void Soldier::fire()
{
    this->gun->shoot();
}

Soldier::~Soldier()
{
    if(this->gun!=NULL)
    {
        delete this->gun;
        this->gun = NULL;
    }
}