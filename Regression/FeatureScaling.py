import numpy as np
import pandas as pd
import matplotlib.pyplot as mp

class FeatureScaling:
	
	def __init__(self,x,y):
		self.x=x.copy()
		if y.ndim==1:
			y=np.reshape(y,(y.shape[0],1))
		self.y=y.copy()


	def fit_scaling_X(self):
		
		features = 0
		for cntr in range(features):
			x_mean=np.mean(self.x[:,features])
			x_min=np.min(self.x[:,features])
			x_max=np.max(self.x[:,features])
			self.x[feature]= (self.x[:,features]-x_mean)/(x_max-x_min)
				
		return self.x



























