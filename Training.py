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
from sklearn.model_selection import cross_val_score
from sklearn.metrics import confusion_matrix
from sklearn import svm
from joblib import dump


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
        #plt.plot(frame)
        #plt.show()
        frame_var = np.var(frame, axis = 0)
        frame_skew = stat.skew(frame, axis = 0)
        frame_kurt = stat.kurtosis(frame, axis = 0)
        frame_gmean = np.transpose(stat.gmean(frame, axis = 0))
        features = np.hstack((frame_var, frame_skew, frame_kurt, frame_gmean)).reshape(-1, 12)
        if np.size(total_features) == 0:
            total_features = features
        else:
            total_features = np.vstack((total_features, features))
    #classify left as 1 and right as 2
    y = np.ones(len(peaks)) * classification
    return total_features, y

def extract_noise(file_name, classification):
    data = np.genfromtxt(file_name, delimiter=',')
    total_features = []
    size = len(data[:,2])
    samples_done = 0
    for i in range(50, size - 50, 25):
        samples_done = samples_done + 1
        frame = data[i - 50: i+50, :]
        frame_var = np.transpose(np.var(frame, axis = 0))
        frame_skew = np.transpose(stat.skew(frame, axis = 0))
        frame_kurt = np.transpose(stat.kurtosis(frame, axis = 0))
        frame_gmean = np.transpose(stat.gmean(frame, axis = 0))
        features = np.hstack((frame_var, frame_skew, frame_kurt, frame_gmean)).reshape(-1, 12)
        if np.size(total_features) == 0:
            total_features = features
        else:
            total_features = np.vstack((total_features, features))
    y = np.ones(samples_done) * classification
    print(y)
    return total_features, y


def train_model(X, y):
   model = svm(n_estimators=20)
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
    print('Entering training.....')

    #extract features from two csv files
    #extract features on :1 but peaks are negative
    features_swipe_left, y_swipe_left = extract_features('TrainingData/swipe_left.csv', 1)
    features_swipe_right, y_swipe_right = extract_features('TrainingData/swipe_right.csv',  2)
    features_hover, y_hover = extract_noise('TrainingData/hover.csv', 3)
    features_jitter, y_jitter = extract_features('TrainingData/jitter.csv', 4)
    features_nothing, y_nothing = extract_noise('TrainingData/nothing.csv', 0)

    #combine data
    y = np.vstack(( y_swipe_left.reshape(-1,1) , y_swipe_right.reshape(-1, 1) , y_hover.reshape(-1, 1), y_jitter.reshape(-1, 1), y_nothing.reshape(-1, 1)))
    X = np.vstack((features_swipe_left, features_swipe_right, features_hover, features_jitter, features_nothing))

    #randomize data
    print('Pre-proc: getting training features...')
    data = np.hstack((X, y))
    np.random.shuffle(data)
    y = data[:,-1]
    X = data[:, :-1]

    #train model
    print('Training model...')
    trained_model = RandomForestClassifier(n_estimators = 20)
    trained_model.fit(X,y)
    cross_val_scores = cross_val_score(trained_model, X, y, cv = 3)
    print(cross_val_scores)
    
    #Predice on model
    print('Validation scores....')
    predictions = trained_model.predict(X)
    print(confusion_matrix(y, predictions))
    print('Finished training....')

if __name__ == '__main__':
    train()
