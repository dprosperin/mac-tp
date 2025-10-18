#include "stm32f3xx.h"
#include "pinAccess.h"

/*
Question 1 :
L'objectif de cette question est d'allumer la led PB3 lorque l'on appuie sur le boutton D6
*/

void wait() {
  volatile int i = 0;
  for (i = 0; i < 2000000; i++)
    ;
}

void setup() {
  // PB3 (led) as output
  pinMode(GPIOB,3, OUTPUT);

  pinMode(GPIOB,1, INPUT_PULLUP);
}

/* main function */
int main(void) {
  setup();
  /* Infinite loop */
  while (1) {
    int btn = digitalRead(GPIOB, 1); // Récupération de la l'état du bouton

    if (!btn)
    {
      digitalWrite(GPIOB,3,1); // Allumage de la Led
    } else {
       digitalWrite(GPIOB,3,0); // Eteindre la Led
    }
  }
}

