#include "stm32f3xx.h"
#include "pinAccess.h"

#define CH0 7
#define CH1 0
#define CH2 1

void wait() {
  volatile int i = 0;
  for (i = 0; i < 2000000; i++)
    ;
}

void setLed(int ledId)
{
  switch (ledId)
  {
  case 0:
    pinMode(GPIOB, CH0, OUTPUT);
    pinMode(GPIOF, CH1, OUTPUT);
    pinMode(GPIOF, CH2, INPUT);

    digitalWrite(GPIOB, CH0, 1);
    digitalWrite(GPIOF, CH1, 0);
    break;

   case 1:
    pinMode(GPIOB, CH0, OUTPUT);
    pinMode(GPIOF, CH1, OUTPUT);
    pinMode(GPIOF, CH2, INPUT);

    digitalWrite(GPIOB, CH0, 0);
    digitalWrite(GPIOF, CH1, 1);
    break;

    case 2:
    pinMode(GPIOB, CH0, INPUT);
    pinMode(GPIOF, CH1, OUTPUT);
    pinMode(GPIOF, CH2, OUTPUT);

    digitalWrite(GPIOF, CH1, 1);
    digitalWrite(GPIOF, CH2, 0);
    break;

    case 3:
    pinMode(GPIOB, CH0, INPUT);
    pinMode(GPIOF, CH1, OUTPUT);
    pinMode(GPIOF, CH2, OUTPUT);

    digitalWrite(GPIOF, CH1, 0);
    digitalWrite(GPIOF, CH2, 1);
    break;

     case 4:
    pinMode(GPIOB, CH0, OUTPUT);
    pinMode(GPIOF, CH1, INPUT);
    pinMode(GPIOF, CH2, OUTPUT);

    digitalWrite(GPIOB, CH0, 1);
    digitalWrite(GPIOF, CH2, 0);
    break;

    case 5:
    pinMode(GPIOB, CH0, OUTPUT);
    pinMode(GPIOF, CH1, INPUT);
    pinMode(GPIOF, CH2, OUTPUT);

    digitalWrite(GPIOB, CH0, 0);
    digitalWrite(GPIOF, CH2, 1);
    break;
  
  default:
    break;
  }
}

void setup() {
  pinMode(GPIOB,1, INPUT_PULLUP);
}

/* main function */
int main(void) {
  setup();
  /* Infinite loop */
  int ledId = 0;
  while (1) {
    int btn = !digitalRead(GPIOB, 1);
    
    if (btn)
    {
      ledId++;
      wait();
    }

    if (ledId == 6) ledId = 0;
    
    setLed(ledId);
  }
}