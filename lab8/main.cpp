#include "stm32f3xx.h"
#include "Adafruit_GFX.h"
#include "Adafruit_ST7735.h"
#include "adc.h"
#include "tft.h"

void setup()
{
	Tft.setup();
	Tft.setTextCursor(4, 1); //col,line
	Tft.print("Hello World! ");

	ADCInit();
}

//this is a simple application that uses the TFT display.
// => it first write a string in the top of the screen (in setup)
// => it writes the ADC value of the potentiometer in green, and
//    refreshes it each time the value differs more than 5.
int main()
{
	static int prevPot = -1;
	setup();
	while(1)
	{
		//potentiometer
		int pot = ADCRead(); //12 bits -> 4096 -> 4 digits
		//update only we value changes significantly
		if(abs(prevPot - pot) > 5)
		{
			//set cursor centered on line 4.
			Tft.setTextCursor(Tft.getTextWidth()/2-2,4);
			Tft.eraseText(4);	//remove previous value (4 digits)
			Tft.print(pot);
			prevPot = pot;
		}
	}
}

