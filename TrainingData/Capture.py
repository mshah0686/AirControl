import matplotlib.pyplot as plt
import serial
import numpy as np
import matplotlib.pyplot as plt
import serial
import numpy as np
import pyautogui

def tracker():
    sample_rate = 100 #hertz
    time = 14 #seconds
    sampleSize = sample_rate * time

    port = '/dev/tty.usbmodem1421'
    ard = serial.Serial(port,9600)
    ard.flushInput()
    acc = np.zeros((sampleSize, 3), dtype = int)
    print('Starting capture')
    try:
        print('inside try')
        for i in range(sampleSize):
            data = ard.readline()
            Data = data[:-2].split(b',')
            print(Data)
            acc[i,0] = int(Data[0])
            acc[i,1] = int(Data[1])
            acc[i,2] = int(Data[2])
            print(sampleSize - i)
        return acc
        ard.close()
    except Exception as e:
        print(e)
        print("exception")
        return acc
    ard.close()

if __name__ == '__main__':
    irData = tracker()
    plt.plot(irData)
    np.savetxt('jitter.csv', irData, delimiter=',', fmt='%d')
    plt.show()