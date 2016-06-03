#include <stdio.h>
#include "lib/robot.h"

int main(void)
{
  Robot bender("Bender");

  printf("Hello World\r\n");
  printf("%s\r\n", bender.toString().c_str());
  
  return 0;
}
