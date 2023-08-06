import numpy as np
from mapyl.preprocessing import PolyExp

class SVM:
    """
    Support Vector Machine instance

    Parameters:
        lr (float): float of the learning rate

        lam (float): float of the regularization parameter
        
        degree (int): int of the poly degree (1 for linear)
    """
    def __init__(self, lr=0.001, lam=0.01, degree=1):
        self.lr = lr
        self.lambda_param = lam
        self.w = None
        self.b = None
        self.degree = degree


    def fit(self, X, y, iters):
        """
        Fits the instance

        Parameters:
            X (ndarray): ndarray of shape (num_samples, num_features) of the input

            y (ndarray): ndarray of shape (num_samples,) of the output

        Returns none
        """
        if self.degree > 1:
            X = PolyExp(self.degree).evalnum(X)
        n_samples, n_features = X.shape
        
        y_ = np.where(y <= 0, -1, 1)
        
        self.w = np.zeros(n_features)
        self.b = 0

        for _ in range(iters):
            for idx, x_i in enumerate(X):
                condition = y_[idx] * (np.dot(x_i, self.w) - self.b) >= 1
                if condition:
                    self.w -= self.lr * (2 * self.lambda_param * self.w)
                else:
                    self.w -= self.lr * (2 * self.lambda_param * self.w - np.dot(x_i, y_[idx]))
                    self.b -= self.lr * y_[idx]


    def predict(self, X):
        """
        Predicts the class of the supplied `X`

        Parameter: 
            X (ndarray): ndarray of shape (num_samples, num_features) to be classified

        Returns: int classifying as 1 or -1
        """
        approx = np.dot(X, self.w) - self.b
        return np.sign(approx)
    