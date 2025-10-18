#! /usr/bin/env python3
# -*- coding: UTF-8 -*-
from math import *

nbVal = 256       #nb values for 90°
nbDataPerLine = 8 #number of values per row

print('/* sin 0 to 90 degree. 256 values')
print(' * format fixed point: 1.15')
print(' **/')
print("const int16_t sinTab["+str(nbVal)+"] = {\n\t",end='')

for idx in range (nbVal):

    val = #TODO - update this line -

    print('0x{val:04x}'.format(val=int(val)),end='')
    if idx != (nbVal-1): #except last value
        print(', ',end="")
        if idx % nbDataPerLine == (nbDataPerLine-1):
            print('\n\t',end='')
print('\n};')

