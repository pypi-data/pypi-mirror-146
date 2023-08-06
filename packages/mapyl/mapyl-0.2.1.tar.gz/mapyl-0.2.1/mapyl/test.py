import numpy as np
from classification import SVM, SoftMaxClasser
from utils import Accuracy, Mode
from data import GenData, SplitData
from preprocessing import Normalizer, StandardScaler, MinMaxScaler
from regression import PolyRegressor
from classification import KNearestNeighbors
from clustering import KMeans
import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn import preprocessing

# from keras.datasets import mnist
# (train_X, train_y), (test_X, test_y) = mnist.load_data()
# Keep these commented when not used, they take too much time to load

"""
This is a test file

Here all the tests are done for the library

it is a mess, but dont worry about it
"""

X = np.array([[0, 0], [0, 0], [1, 1], [1, 1], [0, 0], [1, 1]])

print(SplitData.split(X,y=None, test_percent=0.5))