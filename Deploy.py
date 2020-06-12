###########
# Author: Malav Shah
# ------------------
# Train on gathered data and use model to output values on real time input
############
from threading import Thread
from Training import train, predict
import numpy as np
import scipy.signal as sig
import scipy.stats as stat
from threading import Event
from sklearn.ensemble import RandomForestClassifier
import serial
import time
import matplotlib as plt
from joblib import load

#create buffer full interupt event
buffer_full = Event()

#sample size
buffer_size = 150

#single samle
accX = np.zeros(buffer_size, dtype=float)
accY = np.zeros(buffer_size, dtype=float)
accZ = np.zeros(buffer_size, dtype=float)

buffer = np.zeros((buffer_size, 3))
samples_done = 0


def take_input():
    global accX, accY, accZ, buffer_size, samples_done, buffer
    print('Started reading real time....')
    port = '/dev/tty.usbmodem1421'
    ard = serial.Serial(port,9600)
    ard.flushInput()
    while True:
        data = ard.readline()
        new_sample = np.zeros((1, 3))
        new_sample = np.asarray(data[:-2].split(b','))
        #delete top element of buffer
        buffer = np.delete(buffer, 0, 0)
        #add new sample in (creates a queue)
        buffer = np.vstack((buffer, new_sample))
        samples_done = samples_done + 1
        if(samples_done == buffer_size):
            samples_done = 20
            buffer_full.set()

def analyze():
    global samples_done, buffer
    while True:
        buffer_full.wait(timeout=20)
        frame = np.array(buffer).astype(np.float)
        frame_var = np.var(frame, axis = 0)
        frame_skew = stat.skew(frame, axis = 0)
        frame_kurt = stat.kurtosis(frame, axis = 0)
        #frame_gmean = np.transpose(stat.gmean(frame, axis = 0))
        features = np.hstack((frame_var, frame_skew, frame_kurt, frame_kurt)).reshape(-1, 12)
        prediction =predict(features)
        if(prediction[0] == 1):
            print('Gesture Detected: swipe_left')
            samples_done = 0
        elif(prediction[0] == 2):
            print('Gesture Detected: swipe_right')
            samples_done = 0
        elif(prediction[0] == 3):
            print('Gesture Detected: Hover')
            samples_done = 0
        elif(prediction[0] == 4):
            print('Gesture Detected: jitter')
            samples_done = 0
        buffer_full.clear()


#train model
train()

#create serial input thread
thread_input = Thread(target=take_input)
thread_predict = Thread(target=analyze)
try:
    thread_input.start()
    thread_predict.start()
except Exception as e:
    print(e)

