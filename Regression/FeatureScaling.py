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

		if len(self.x.shape) > 1:
			features = self.x.shape[1]
		else:
			features=0
		
		for cntr in range(features):
			x_mean=np.mean(self.x[:,cntr])
			x_min=np.min(self.x[:,cntr])
			x_max=np.max(self.x[:,cntr])
			self.x[:,cntr]= (self.x[:,cntr]-x_mean)/(x_max-x_min)
				
		return self.x

	def fit_scaling_Y(self):

		if len(self.y.shape) > 1:
			features = self.y.shape[1]
		else:
			features=0
		
		for cntr in range(features):
			y_mean=np.mean(self.y[:,cntr])
			y_min=np.min(self.y[:,cntr])
			y_max=np.max(self.y[:,cntr])
			self.y[:,cntr]= (self.y[:,cntr]-y_mean)/(y_max-y_min)
				
		return self.y

























