#include "stm32f3xx.h"
#include "pinAccess.h"

void wait()
{
    volatile int i=0;
    for(i=0;i<2000000;i++);
}

void setup()
{
    pinMode(GPIOB,3,OUTPUT);
}

/* main function */
int main(void)
{
    setup();
    /* Infinite loop */
    while (1)
    {
        digitalToggle(GPIOB,3);
        wait();
    }
}
