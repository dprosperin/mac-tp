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

#for retinal persistence.
led = [False,False,False,False,False,False]

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args,**kwargs)
        self.setWindowTitle("QEmu Ultrasound lab")
        self.leds = [] #PB0, PB3 => tuple (pin,chkbox)
        self.buttons = [] #PB6, PB1 => tuple (pin,chkbox)
        self.warning = 0 # 0 = ok, 1 warning, 2 error
        # bits 0 to 2 are led dirs, bits 4 to 6 are led States 
        self.charliePlexingState = 0
        layoutV = QVBoxLayout()
        self.palOn = QPalette()
        self.palOn.setColor(QPalette.Base,Qt.darkGreen)
        self.palOff = QPalette()
        self.palOff.setColor(QPalette.Base,Qt.darkRed)

        self.palError = QPalette()
        self.palError.setColor(QPalette.Window,Qt.red)
        self.palWarning = QPalette()
        self.palWarning.setColor(QPalette.Window,Qt.darkRed)

        gbox=QGroupBox("user leds")
        #Gpio pin state
        #led D3
        layout = QHBoxLayout()
        chkbox_LED_D3=QCheckBox("D3 (PB0)")
        chkbox_LED_D3.setCheckable(False)
        chkbox_LED_D3.setAutoFillBackground(True)
        chkbox_LED_D3.setPalette(self.palOff)
        self.leds.append((0,chkbox_LED_D3))
        layout.addWidget(chkbox_LED_D3)
        #Gpio pin state
        #led D13
        chkbox_LED_D13=QCheckBox("D13 (PB3)")
        chkbox_LED_D13.setCheckable(False)
        chkbox_LED_D13.setAutoFillBackground(True)
        chkbox_LED_D13.setPalette(self.palOff)
        self.leds.append((3,chkbox_LED_D13))
        layout.addWidget(chkbox_LED_D13)

        gbox.setLayout(layout)
        layoutV.addWidget(gbox)

        gbox=QGroupBox("push buttons")
        #Gpio pin state
        #led D3
        layout = QHBoxLayout()
        chkbox_PB_D5=QCheckBox("D5 (PB6)")
        chkbox_PB_D5.setCheckable(True)
        self.buttons.append((6,chkbox_PB_D5))
        layout.addWidget(chkbox_PB_D5)
        #Gpio pin state
        #led D13
        chkbox_PB_D6=QCheckBox("D6 (PB1)")
        chkbox_PB_D6.setCheckable(True)
        self.buttons.append((1,chkbox_PB_D6))
        layout.addWidget(chkbox_PB_D6)

        gbox.setLayout(layout)
        layoutV.addWidget(gbox)
        for i,pb in self.buttons:
            pb.stateChanged.connect(lambda x, i=i: self.buttonChecked(x,i))

        gbox=QGroupBox("serial")
        layout = QHBoxLayout()
        self.serial = QTextEdit()
        self.serial.setReadOnly(True)
        layout.addWidget(self.serial)
        gbox.setLayout(layout)
        layoutV.addWidget(gbox)

        #ADC pin state
        gbox=QGroupBox("ADC - potentiometer")
        layout = QHBoxLayout()
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(4095)
        layout.addWidget(self.slider)
        self.labelADC = QLabel('0')
        self.slider.valueChanged.connect(self.updateSlider)
        layout.addWidget(self.labelADC)
        gbox.setLayout(layout)
        layoutV.addWidget(gbox)

        widget = QWidget()
        widget.setLayout(layoutV)

        self.setCentralWidget(widget)

    @pyqtSlot()
    def reset(self):
        """called by QEmu at startup. It should send back information to QEmu """
        print('reset')
        for (pin,chkbox) in self.leds:
            chkbox.setPalette(self.palOff)
        for (pin,chkbox) in self.buttons:
            chkbox.setCheckState(Qt.Unchecked)
        self.serial.clear()
        self.slider.setValue(0)

    def buttonChecked(self,state,pin):
        """ called when a checkbox is checked """
        gpioId = 1 #2 buttons on GPIOB
        #print("send msg: GPIO "+str(gpioId)+", pin "+str(pin)+', state '+str(state==Qt.Checked) )
        s=struct.pack("=IIII",pipc_gpio_magic,pin,state==Qt.Checked,gpioId)
        mq_to_qemu.send(s)

    def updateSlider(self,val):
        """ called each time the slider value is updated
        """
        self.labelADC.setText(str(val))
        #print("send msg to ADC 0:"+str(val))
        s=struct.pack("=III",pipc_adc_magic,0,val)
        mq_to_qemu.send(s)

    def setGPIO(self,port,dir_mask,output):
        #print('gpio '+str(port)+', dir'+str(dir_mask)+', out'+str(output))
        if port == 'B': #pin0 is PB7 
            for (pin,widget) in self.leds:
                pinMask = 1<<pin
                if (dir_mask & pinMask == pinMask) and (output & pinMask == pinMask):
                    widget.setPalette(self.palOn)
                else:
                    widget.setPalette(self.palOff)

app = QApplication(sys.argv)
window = MainWindow()

class Receiver(QThread):
    resetSig  = pyqtSignal()
    gpioSig   = pyqtSignal(str,int,int)
    serialSig = pyqtSignal(str)

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
                magic, char = struct.unpack("=II",msg[0])
                self.serialSig.emit(chr(char & 0xff))
            elif magic[0] == pipc_mcp_magic:
                pass
            elif magic[0] == pipc_reset_magic:
                self.resetSig.emit()
            else:
                raise Exception("Wrong magic number in GPIO IPC message: 0x{val:08x}".format(val=magic[0]) )
            #required if we get too many messages to let time for the UI.
            time.sleep(.01)

def warningPersistence():
    while True:
        time.sleep(2)
        if window.warning > 0:
            window.warning = 0
            #print('reinit')

window.show()

thread = Receiver()
thread.resetSig.connect(window.reset)
thread.gpioSig.connect(window.setGPIO)
thread.serialSig.connect(window.serial.insertPlainText)
thread.start()

threadWarning = threading.Thread(target=warningPersistence)
threadWarning.daemon = True
threadWarning.start()

app.exec_() #event loop
