import numpy as np
from mapyl.utils import Mode

class KNearestNeighbors:
    """
    KNearest Neighbors instance for classification

    Parameter: 
        K (int): the number of nearest neighbors
    """
    def __init__(self, K=5):
        self.K = K
    
    def fit(self, X, y):
        """
        Fits the instance

        Parameters:
            X (ndarray): ndarray of shape (num_samples, num_features) of the input

            y (ndarray): ndarray of shape (num_samples,) of the output
        
        Returns none
        """
        self.X_t = X
        self.y_t = y
        self.m_t, self.n = X.shape

    def predict(self, X):
        """
        Predicts the class of a X value

        Parameter:
            X (ndarray): The X values to be predicted

        Returns:
            int: The index of the class of the supplied X
        """
        self.X = X
        self.m, self.n = X.shape
        y_pred = np.zeros(self.m)
        for i in range(self.m) :   
            x = self.X[i]
            neighbors = np.zeros(self.K)
            neighbors = self._find_neighbors(x)
            y_pred[i] = Mode.mode(neighbors)[0][0]    
        return y_pred
    
    def _find_neighbors(self, x):
        euclidean_distances = np.zeros(self.m_t)
        for i in range(self.m_t):
            d = self._euclidean(x, self.X_t[i])  
            euclidean_distances[i] = d
        inds = euclidean_distances.argsort()
        y_t_sort = self.y_t[inds]
        return y_t_sort[:self.K]
    
    def _euclidean(self, X, X_t):
        return np.sqrt(np.sum(np.square(X - X_t)))