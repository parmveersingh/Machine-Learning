import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class LinearRegression:
	
	def __init__(self,x,y):
		ones=np.ones([x.shape[0],1],dtype=int)
		self.x=np.append(ones,x,axis=1)
		self.y=y
		self.theta=np.random.randn(self.x.shape[1])


	def return_theta(self):
	
		return self.theta


	def cost_function(self):
		
		h=np.matmul(self.x,self.theta)
		self.j=(1/(2*(self.x.shape[0])))*(np.sum((h-self.y[:,0])**2))
		return self.j


	def gradient(self,iters,alpha):
		
		alpha_history = []
		cost_history =[]
		thetas = []
		theta=self.theta
		for i in range(iters):
			h=np.matmul(self.x,self.theta)
			j=self.cost_function()
			cost_history.append(j)
			alpha_history.append(theta)
			theta[1]=theta[1]-((alpha/self.x.shape[0])*np.sum(np.multiply((h-self.y[:,0]),self.x[:,1])))
			theta[0]=theta[0]-((alpha/self.x.shape[0])*np.sum(h-self.y[:,0]))
		
		for i in range(2):
			thetas.append(theta[i])
		
		return thetas,cost_history,alpha_history

	def predict(self,test_x,theta_get,test_y):
		
		ones=np.ones([test_x.shape[0],1],dtype=int)
		self.x_test= np.append(ones,test_x,axis=1)
		y_pred= np.matmul(self.x_test,theta_get)
		error_pred = (abs(test_y-y_pred)/test_y)*100 
		return y_pred,error_pred
		
