#ifndef __sw_h__
#define __sw_h__

#include <stdint.h>

/* Init stopwatch. Should be called first (during setup)
 * Works at CPU clock speed (64MHz) to count instruction cycles
 * */
void SWInit();
/* Reset stopwatch. It will restart counter from 0 */
void SWReset();
/* Get the 32 bit value of the stopwatch 
 * Expire in ~67s
 * */
uint32_t SWGet();

#endif
