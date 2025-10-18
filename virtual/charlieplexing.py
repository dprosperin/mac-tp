#! /usr/bin/env python3
# -*- coding: UTF-8 -*-

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import sys,time

import threading
# Communication part
import struct
pipc_gpio_magic    = 0xdeadbeef
pipc_adc_magic     = 0xcafecafe
pipc_serial_magic  = 0xabcdef01
pipc_mcp_magic     = 0xfeedfeed
pipc_reset_magic   = 0xbadf00d

import posix_ipc as pipc
mq_to_qemu = pipc.MessageQueue("/to_qemu",flags=pipc.O_CREAT, read=False, write=True)
mq_from_qemu = pipc.MessageQueue("/from_qemu",flags=pipc.O_CREAT, read=True, write=False)


class MainWindow(QMainWindow):
    #for retinal persistence.
    led = [False,False,False,False,False,False]

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args,**kwargs)
        self.setWindowTitle("QEmu GPIO interface for STM32F303 - Charlipexing")
        self.leds = []
        # bits 0 to 2 are led dirs, bits 4 to 6 are led States 
        self.charliePlexingState = 0
        layoutV = QVBoxLayout()
        self.palOn = QPalette()
        self.palOn.setColor(QPalette.Base,Qt.darkGreen)
        self.palOff = QPalette()
        self.palOff.setColor(QPalette.Base,Qt.darkRed)

        gbox=QGroupBox("Charlieplexing")
        #Gpio pin state
        layout = QHBoxLayout()
        for i in range(6):
            chkbox=QCheckBox("L"+str(i))
            chkbox.setCheckable(False)
            chkbox.setAutoFillBackground(True)
            chkbox.setPalette(self.palOff)
            self.leds.append(chkbox)
            layout.addWidget(chkbox)
        gbox.setLayout(layout)
        layoutV.addWidget(gbox)

        widget = QWidget()
        widget.setLayout(layoutV)

        self.setCentralWidget(widget)

    @pyqtSlot()
    def reset(self):
        """called by QEmu at startup. It should send back information to QEmu """
        print('reset')
        for chkbox in self.leds:
            chkbox.setPalette(self.palOff)

    def setGPIO(self,port,dir_mask,output):
        update = False
        if port == 'B': #pin0 is PB7 
            self.charliePlexingState &= ~0x9 #raz bit 0 and 3 
            self.charliePlexingState |= (dir_mask >> 7) & 1
            self.charliePlexingState |= ((output   >> 7) & 1) << 3
            update = True
        if port == 'F': #pin1,2 is PF0,1 
            self.charliePlexingState &= ~0x36 # raz bit 1,2,4, 5
            self.charliePlexingState |= (dir_mask & 3) << 1 #set bits 1,2
            self.charliePlexingState |= (output   & 3) << 4 #set bits 4,5
            update = True
        if update:
            mask=[0x1B,0x1B,0x36,0x36,0x2D,0x2D]
            data=[0x0B,0x13,0x16,0x26,0x0D,0x25]
            #Leds
            for l in range(6):
                if (self.charliePlexingState & mask[l]) == data[l]:
                    self.leds[l].setPalette(self.palOn)
                    self.led[l] = True
                else:
                    self.led[l] = False
                
    @pyqtSlot()
    def switchLedOffs(self):
        for i in range(6):
            if not self.led[i]:
                window.leds[i].setPalette(window.palOff)
            #self.led[i] = False

app = QApplication(sys.argv)
window = MainWindow()

class Receiver(QThread):
    resetSig  = pyqtSignal()
    gpioSig   = pyqtSignal(str,int,int)

    def __init__self():
        QThread.__init__(self)

    def run(self):
        while True:
            msg = mq_from_qemu.receive()
            magic = struct.unpack("=I",msg[0][0:4]) #get magic value. return a tuple.
            #print("mg=",mg," pin=",pin," gpio=",gpio," state=",state) 
            if magic[0] == pipc_gpio_magic:
                magic, changed_out, dir_mask,output,gpio = struct.unpack("=IHHHH",msg[0])
                name = ['A','B','C','D','F']
                if gpio < 5:
                    self.gpioSig.emit(name[gpio],dir_mask,output)
            elif magic[0] == pipc_serial_magic:
                pass
            elif magic[0] == pipc_mcp_magic:
                pass
            elif magic[0] == pipc_reset_magic:
                self.resetSig.emit()
            else:
                raise Exception("Wrong magic number in GPIO IPC message: 0x{val:08x}".format(val=magic[0]) )
            #required if we get too many messages to let time for the UI.
            time.sleep(.01)

class RetinalPersistence(QThread):
    switchOffLedSig  = pyqtSignal()
    def __init__self():
        QThread.__init__(self)
    def run(self):
        while True:
            time.sleep(0.3)
            self.switchOffLedSig.emit()

window.show()

thread = Receiver()
thread.resetSig.connect(window.reset)
thread.gpioSig.connect(window.setGPIO)
thread.start()

threadPersistence = RetinalPersistence()
threadPersistence.switchOffLedSig.connect(window.switchLedOffs)
threadPersistence.start()

app.exec_() #event loop
