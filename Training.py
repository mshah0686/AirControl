###########
# Author: Malav Shah
# ------------------
# Train data on gathered truth data using RandomForrestClassifier
############

import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as sig
import scipy.stats as stat
from sklearn.ensemble import RandomForestClassifier
from sklearn import svm
from sklearn.model_selection import cross_val_score
from sklearn.metrics import confusion_matrix


total_features = []

def extract_features(file_name, classification):
    data = np.genfromtxt(file_name, delimiter=',')
    total_features = []
    print('Extracting features')

    #find peak based on right reader
    peaks,_ = sig.find_peaks(data[:,2], height = 200)
    for peak in peaks:
        #f is the sub frame of the peak (certain parameter left and right of it)
        frame = data[peak-50:peak+50, :]
        plt.plot(frame)
        plt.show()
        frame_var = np.var(frame, axis = 0)
        frame_skew = stat.skew(frame, axis = 0)
        frame_kurt = stat.kurtosis(frame, axis = 0)
        features = np.hstack((frame_var, frame_skew, frame_kurt))
        if np.size(total_features) == 0:
            total_features = features
        else:
            total_features = np.vstack((total_features, features))
    #classify left as 1 and right as 2
    y = np.ones(len(peaks)) * classification
    return total_features, y

def extract_noise(filename, classification):
    data = np.genfromtxt(file_name, delimiter=',')
    total_features = []
    size = len(data[:,2])
    samples_done = 0
    for i in range(40, size - 50, 25):
        samples_done = samples_done + 1
        frame = data[i - 50: i+50, :]
        frame_var = np.var(frame, axis = 0)
        frame_skew = stat.skew(frame, axis = 0)
        frame_kurt = stat.kurtosis(frame, axis = 0)

        features = np.hstack((frame_var, frame_skew, frame_kurt))
        if np.size(total_features) == 0:
            total_features = features
        else:
            total_features = np.vstack((total_features, features))
    y = np.ones(samples_done) * classification
    return total_features, y


def train_model(X, y):
   model = RandomForestClassifier(n_estimators=20)
   cross_val_scores = cross_val_score(model, X, y, cv = 3)
   print(cross_val_scores)

   model.fit(X, y)
   return model

#given a set of features, return a prediction
def predict(features):
    global trained_model
    return trained_model.predict(features)

global trained_model

#Extract features and return a trained model
def train():
    global trained_model
    #trained_model = RandomForestClassifier(n_estimators=200)
    trained_model = svm.SVC()
    print('Entering training.....')

    #extract features from two csv files
    #extract features on :1 but peaks are negative
    features_swipe_left, y_swipe_left = extract_features('TrainingData/swipe_left.csv', 1)
    features_swipe_left, y_swipe_right = extract_features('TrainingData/swipe_right.csv',  2)
    features_hover, y_hover = extract_noise('TrainingData/hover.csv', 3)
    features_jitter, y_jitter = extract_features('TrainingData/jitter.csv', 4)
    
    #combine data
    y = np.vstack(( y_left.reshape(-1,1) , y_right.reshape(-1, 1) , y_up.reshape(-1, 1), y_noise.reshape(-1, 1)))
    X = np.vstack((features_left, features_right, features_up, features_noise))
    
    #randomize data
    print('Pre-proc: getting training features...')
    data = np.hstack((X, y))
    np.random.shuffle(data)
    y = data[:,-1]
    X = data[:, :-1]

    #train model
    print('Training model...')
    trained_model = train_model(X,y)

    #create validation set data
    #cv_x, cv_y = extract_features('cv_set.csv')
    #print(len(cv_y))
    #cv_x = np.vstack((cv_x, total_features_neg))
    #cv_y = np.append(cv_y, y_neg)
    
    #Predice on model
    print('Validation scores....')
    predictions = trained_model.predict(X)
    print(confusion_matrix(y, predictions))
    print('Finished training....')

if __name__ == '__main__':
    train()
