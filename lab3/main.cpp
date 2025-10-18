#include "stm32f3xx.h"
#include "sw.h"
#include "Adafruit_GFX.h"
#include "Adafruit_ST7735.h"
#include "tft.h"

/** affichage d'une valeur 
 *  au format virgule fixe 10.6
 */
void affVF10_6(int16_t val)
{
	//seul endroit avec des 'float' car c'est du debug!!
	Tft.print(((float)(val))/64);
}

void setup() {
    SWInit();
    Tft.setup();
}

int main(void) {

    volatile int temps;
    setup();

    Tft.setTextCursor(5,0);

    SWReset();
    for(int i=0;i<10000;i++);
    temps = SWGet();
    Tft.print(temps);

    /* Infinite loop */
    while (1) {

    }
}

