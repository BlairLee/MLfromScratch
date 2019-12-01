""""
Author : Aditya Jain
Contact : https://adityajain.me
"""
import numpy as np
import matplotlib.pyplot as plt

class SGDRegressor():
	"""
	SGD regressor model, that optimizes using gradient descent

	Parameters
	----------
	seed : integer, random seed
	normalize : boolean, normalize X in fit method

	Attributes
	----------
	coef_ : Estimated coefficients for the linear regression problem
	intercept_ : integer, bias for the linear regression problem

	"""
	def __init__(self,seed=None,normalize=False):
		self.W = None
		self.b = None
		self.__length = None
		self.__normalize = normalize
		self.__m = None
		self.__costs = []
		self.__iterations = []
		np.random.seed(seed if seed is not None else np.random.randint(100))

	def __initialize_weights_and_bais(self):
		self.W = np.random.randn(self.__length) #(n,1)
		self.b = 0
        
	def __computeCost(self,h,Y):
		loss = np.square(h-Y)
		cost = np.sum(loss)/(2*self.__m)
		return cost

	def __optimize(self,X,Y,lr=None):
		h = np.dot(X,self.W)+self.b
		dW = np.dot( X.T, (h-Y) ) / self.__m
		db = np.sum( h-Y )  / self.__m
		self.W = self.W - lr*dW
		self.b = self.b - lr*db

	def __normalizeX(self,X): return (X-self.__mean) / (self.__std)
	
	def fit(self, X, y, lr=0.01, tol=0.01, verbose=False):
		"""
		Fit X using y by optimizing weights and bias
		
		Parameters
		----------
		X : 2D numpy array, independent variables
		y : 1D numpy array, dependent variable
		lr : float, learning rate (Default 0.01)
		tol : float, tolerance as stopping criteria for gradient descent (Default : 0.01)
		verbose : boolean, print out details while optimizing (Default : False) 
		
		"""
		if self.__normalize:
			self.__mean, self.__std = X.mean(axis=0), X.std(axis=0)
			X = self.__normalizeX(X)
		self.__m,self.__length = X.shape
		self.__initialize_weights_and_bais()
		last_cost,i = float('inf'),0
		while True:
			h = np.dot(X,self.W)+self.b
			cost = self.__computeCost(h,y)
			if verbose: print(f"Iteration: {i}, Cost: {cost:.3f}")
			self.__optimize(X,y,lr=lr)
			if last_cost-cost < tol: break
			else: last_cost,i = cost,i+1
			self.__costs.append(cost)
			self.__iterations.append(i)

	def predict(self,X):
		"""
		Predict dependent variable
		
		Parameters
		----------
		X : numpy array, independent variables

		Output
		------
		precicted values
		
		"""
		if self.__normalize: X = self.__normalizeX(X)
		return np.dot(X,self.W)+self.b

	def plot(self,figsize=(7,5)):
		"""
		Plot a optimization graph
		"""
		plt.figure(figsize=figsize)
		plt.plot(self.__iterations,self.__costs)
		plt.xlabel('Iterations')
		plt.ylabel('Cost')
		plt.title("Iterations vs Cost")
		plt.show()

	def score(self,X,y):
		"""
		Computer Coefficient of Determination (rsquare)

		Parameters
		----------
		X : 2D numpy array, independent variables
		y : numpy array, dependent variables

		Output
		------
		r2 values
		
		"""
		return 1-(np.sum(((y-self.predict(X))**2))/np.sum((y-np.mean(y))**2))

	@property
	def coef_(self): return self.W

	@property
	def intercept_(self): return self.b