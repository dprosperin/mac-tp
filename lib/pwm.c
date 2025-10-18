#include "pwm.h"

int PWMEnableChannel(TIM_TypeDef *tim, int channel)
{
  //check args
  if(!IS_TIM_INSTANCE(tim)) return -1;
  if((channel < 1) || (channel >4)) return -2;
  //config reg access
  __IO uint32_t *CCMRx;
  if(channel < 3) CCMRx = &(tim->CCMR1);
  else CCMRx = &(tim->CCMR2);
  int offset = 0;
  if((channel & 1) == 0)//2 ou 4
  {
    offset = 8;
  }
  //reset fields
  *CCMRx &= ~(0x3 << offset);      //CCxS = 0
  *CCMRx &= ~(0x7 << (offset+4));  //CCxM[2..0] = 0 
  *CCMRx &= ~(0x1 << (offset+16)); //CCxM[3] = 0
  //output PWM mode 1
  *CCMRx |=   6 << (offset+4);     //CCxM = 0b0110
  //pre-load register TIMx_CCRy
  *CCMRx |=   1 << (offset+3);     //CCxPE = 1
  //mode 1 - edge aligned mode
  tim->CR1 &= ~TIM_CR1_CMS_Msk;
  //enable channel
  tim->CCER |= 1 << (4*(channel-1)); //offset 0, 4, 8 and 12

  return 0;
}
