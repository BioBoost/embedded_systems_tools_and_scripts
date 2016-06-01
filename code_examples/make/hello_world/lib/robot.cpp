#include "robot.h"

Robot::Robot(std::string name)
{
  this->name = name;
}

std::string Robot::toString(void)
{
  return "I am a Robot called " + this->name;
}
