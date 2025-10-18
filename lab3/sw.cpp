#include "stm32f3xx.h"

void SWInit() //init stopwatch
{
  RCC->APB1ENR |= RCC_APB1ENR_TIM2EN;
  __asm("nop");
  RCC->APB1RSTR |=  RCC_APB1RSTR_TIM2RST;
  RCC->APB1RSTR &= ~RCC_APB1RSTR_TIM2RST;
  // configure TIM6
  TIM2->PSC = 0;            // full speed: 64MHz
  TIM2->EGR = TIM_EGR_UG;   // update event => load PSC
  TIM2->CNT = 0;
  TIM2->CR1 = TIM_CR1_CEN; //enable, all other fields to 0
}

void SWReset() { // reset CNT
  TIM2->CNT = 0;
}

uint32_t SWGet() { // get value;
  return TIM2->CNT;
}
