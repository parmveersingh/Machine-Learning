import numpy as np
import pandas as pd

class Feature_Scaling:

	def __init__(self,x,y):
		
		self.x=x
		self.y=y

	def feature_x(self):
		feature= self.x.shape[1]
		self.mean_x=[]
		self.maximum_x=[]
		self.minimum_x=[]		
		for i in range(feature):
			self.mean_x.append(np.mean(self.x[:,i]))
			self.maximum_x.append(np.max(self.x[:,i]))
			self.minimum_x.append(np.min(self.x[:,i]))
			self.x[:,i]=(self.x[:,i]-self.mean_x[i])/(self.maximum_x[i]-self.minimum_x[i])
		return self.x

	def feature_y(self):
		if len(self.y.shape) > 1:
			feature= self.y.shape[1]
		else:
			feature=0
		self.mean_y=[]
		self.maximum_y=[]
		self.minimum_y=[]		
		for i in range(feature):
			self.mean_y.append(np.mean(self.y[:,i]))
			self.maximum_y.append(np.max(self.y[:,i]))
			self.minimum_y.append(np.min(self.y[:,i]))
			self.y[:,i]=(self.y[:,i]-self.mean_y[i])/(self.maximum_y[i]-self.minimum_y[i])
		return self.y
# 1/1+e()

	def rev_feature_y(self,test_y):

		if len(test_y.shape) > 1:
			feature= test_y.shape[1]
		else:
			feature=0
		
		for i in range(feature):
			test_y[i]=test_y[i]*(self.maximum_y[i]-self.minimum_y[i])+self.mean_y[i]
		return test_y
