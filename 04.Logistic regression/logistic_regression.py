import numpy as np
import pandas as pd

class Logistic_Regression:

	def __init__(self,x,y):

		one=np.ones([x.shape[0],1])
		self.x=np.append(one,x,axis=1)
		self.y=y
		self.theta=np.zeros(self.x.shape[1])

	
	def equation(self):

		h=1/(1+np.exp(np.matmul(self.x,self.theta)))
		return h
		
	
	def cost_function(self):
		
		h=self.equation()
		cost=(-np.matmul(self.y,np.log(h)))-(np.matmul((1-self.y),np.log(1-h)))
		return cost

	
	def gradient(self,iters,alpha):
		
		y=self.y

		for i in range(iters):
			h=self.equation()	
			for j in range(self.theta.size):
				self.theta[j]=self.theta[j]-(alpha/self.x.shape[0])*(np.sum(np.matmul((h-y),self.x[:,j])))
			
		return self.theta

	def pred(self,theta,test_x,test_y):
		one=np.ones([test_x.shape[0],1])
		test_x=np.append(one,test_x,axis=1)
		
		pred_y=1/(1+np.exp(-(np.matmul(test_x,theta))))
		return pred_y
