#pragma once

#include <string>

class Robot
{
  private:
    std::string name;

  public:
    Robot(std::string name);

  public:
    std::string toString(void);
};
