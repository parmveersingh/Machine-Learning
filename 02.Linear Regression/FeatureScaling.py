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
		self.y_mean=[]
		self.y_min=[]
		self.y_max=[]
		if len(self.y.shape) > 1:
			features = self.y.shape[1]
		else:
			features=0
		
		for cntr in range(features):
			
			self.y_mean.append(np.mean(self.y[:,cntr]))
			self.y_min.append(np.min(self.y[:,cntr]))
			self.y_max.append(np.max(self.y[:,cntr]))
			self.y[:,cntr]= (self.y[:,cntr]-self.y_mean[cntr])/(self.y_max[cntr]-self.y_min[cntr])
		return self.y	



	def inverse_fit_scaling_Y(self,y_pred):
		if y_pred.ndim==1:
			y_pred=np.reshape(y_pred,(y_pred.shape[0],1))

		if len(y_pred.shape) > 1:
			features = y_pred.shape[1]
		else:
			features=0
		
		
		for cntr in range(features):
			y_pred[:,cntr]= y_pred[:,cntr]*(self.y_max[cntr]-self.y_min[cntr])+self.y_mean[cntr]
		return y_pred

























