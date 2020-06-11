import matplotlib.pyplot as plt
import serial
import numpy as np
import matplotlib.pyplot as plt
import serial
import numpy as np
import pyautogui

def tracker():
    sample_rate = 100 #hertz
    time = 2 #seconds
    sampleSize = sample_rate * time

    port = '/dev/tty.usbmodem1421'
    hexi = serial.Serial(port,9600)
    hexi.flushInput()
    print('Starting capture')
    previous = 0
    while True:
        data = hexi.readline()
        Data = data[:-2].split(b',')
        try:
            if int(Data[0]) > 300:
                pyautogui.move(-6, 0, 0.0001)
                hexi.flushInput()
                print('left')
            if int(Data[1]) > 300:
                hexi.flushInput()
                print('middle')
            if int(Data[2]) > 300:
                pyautogui.move(6,0, 0.0001)
                hexi.flushInput()
                print('right')
            else:
                previous = -1
        except:
            pass
    hexi.close()

if __name__ == '__main__':
    tracker()