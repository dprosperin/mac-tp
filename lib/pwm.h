#ifndef __PWM_H__
#define __PWM_H__

#include "stm32f3xx.h"

/**
 * PWM Enable Channel
 * @param tim: the timer instance (TIM2, TIM3, ...)
 * @param channel: PWM channel, between 1 and 4
 * @return 0 in case of success, -1 or -2 if param timer or channel are incorrect, respectively
 * 
 * To use the PWM:
 * - first configure the alternative pin: pinAlt()
 * - then configure the timer: PSC, ARR, …
 * - then enable the PWM channel: PWMEnableChannel()
 * - set duty value : TIMx->CCRy = ...;
 * - and start timer: TIMx->CR1 |= TIM_CR1_CEN; 
*/
#ifdef __cplusplus
 extern "C" {
#endif

int PWMEnableChannel(TIM_TypeDef *tim, int channel);

#ifdef __cplusplus
}
#endif


#endif