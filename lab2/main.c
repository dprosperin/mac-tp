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
    pinMode(GPIOF, CH2, INPUT);
    pinMode(GPIOB, CH0, INPUT);
    pinMode(GPIOF, CH1, INPUT);

  switch (ledId)
  {
  case 0:
    pinMode(GPIOF, CH2, INPUT);
    pinMode(GPIOB, CH0, OUTPUT);
    pinMode(GPIOF, CH1, OUTPUT);

    digitalWrite(GPIOB, CH0, 1);
    digitalWrite(GPIOF, CH1, 0);
    break;

   case 1:
    pinMode(GPIOF, CH2, INPUT);
    pinMode(GPIOB, CH0, OUTPUT);
    pinMode(GPIOF, CH1, OUTPUT);

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
    pinMode(GPIOF, CH1, INPUT);
    pinMode(GPIOB, CH0, OUTPUT);
    pinMode(GPIOF, CH2, OUTPUT);

    digitalWrite(GPIOB, CH0, 1);
    digitalWrite(GPIOF, CH2, 0);
    break;

    case 5:
    pinMode(GPIOF, CH1, INPUT);
    pinMode(GPIOB, CH0, OUTPUT);
    pinMode(GPIOF, CH2, OUTPUT);

    digitalWrite(GPIOB, CH0, 0);
    digitalWrite(GPIOF, CH2, 1);
    break;
  
  default:
    break;
  }
}

void charlieplexing(uint8_t mask)
{
  if (mask & 0x20)
    setLed(0);

  if (mask & 0x10)
    setLed(1);
  
  if (mask & 0x8)
    setLed(2);

  if (mask & 0x4)
    setLed(3);

  if (mask & 0x2)
    setLed(4);

  if (mask & 0x1)
    setLed(5);
}

void setup() {
  pinMode(GPIOB,1, INPUT_PULLUP);
  pinMode(GPIOB,6, INPUT_PULLUP);
}

/* main function */
int main(void) {
  setup();
  /* Infinite loop */
  int pasAllume = 0;
  while (1) {
    int btn = !digitalRead(GPIOB, 1);
    int btn2 = !digitalRead(GPIOB, 6);

    if (btn)
    {
      pasAllume++;
      wait();
    } else if (btn2)
    {
      pasAllume--;
      wait();
    }
    
    switch (pasAllume)
    {
    case 0:
      setLed(1);
      setLed(2);
      setLed(3);
      setLed(4);
      setLed(5);
      break;

    case 1:
      setLed(0);
      setLed(2);
      setLed(3);
      setLed(4);
      setLed(5);
      break;

    case 2:
      setLed(0);
      setLed(1);
      setLed(3);
      setLed(4);
      setLed(5);
      break;
    
    case 3:
      setLed(0);
      setLed(1);
      setLed(2);
      setLed(4);
      setLed(5);
      break;

    case 4:
      setLed(0);
      setLed(1);
      setLed(2);
      setLed(3);
      setLed(5);
      break;

    case 5:
      setLed(0);
      setLed(1);
      setLed(2);
      setLed(3);
      setLed(4);
      break;
    
    default:
      break;
    }

    if (pasAllume > 5) pasAllume = 0;
    if (pasAllume < 0) pasAllume = 5;
  }
}