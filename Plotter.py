import matplotlib.pyplot as plt
import serial
import numpy as np


import matplotlib.pyplot as plt
import serial
import numpy as np

def captureSerialData():
    sample_rate = 100 #hertz
    time = 2 #seconds
    sampleSize = sample_rate * time

    port = '/dev/tty.usbmodem1421'
    acc = np.zeros((sampleSize, 3), dtype = int)
    hexi = serial.Serial(port,9600)
    hexi.flushInput()
    print('Starting capture')
    for i in range(sampleSize):
        data = hexi.readline()
        Data = data[:-2].split(b',')
        print(Data)
        acc[i,0] = Data[0]
        acc[i, 1] = Data[1]
        acc[i, 2] = Data[2]
        print(sampleSize - i)
    return acc
    hexi.close()

if __name__ == '__main__':
    accData = captureSerialData()
    plt.plot(accData)
    np.savetxt('flik_up.csv', accData, delimiter=',', fmt='%d')
    plt.show()