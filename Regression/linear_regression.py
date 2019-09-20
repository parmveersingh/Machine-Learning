import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class LinearRegression:
	
	def __init__(self,x,y):
		ones=np.ones([x.shape[0],1],dtype=int)
		self.x=np.append(x,ones,axis=1)
		self.y=y
		self.theta=np.random.randn(self.x.shape[0])


	def return_theta(self):
	
		return self.theta


	def cost_function(self):

		#h=np.matmul(self.x,self.theta)
		h1= (self.x.T)*(self.theta)
		#print(h)
		print(h1)
		self.j=(1/2*(self.x.shape[0]))*np.sum((h-self.y)**2)
		return self.j


	def gradient(self,iters,alpha):
		
		self.alpha_history = []
		self.cost_history =[]

		for i in range(iters):
			h=np.matmul(self.x,self.theta) 
			print("theta")
			anys=np.sum(h-self.y)
			print(sum(self.x[:,0]*anys))
			print(self.theta)
			
			j=self.cost_function()
			self.cost_history.append(j)
			self.alpha_history.append(self.theta)
			self.theta = self.theta-(alpha/(self.x.shape[0]))*(self.x.T.dot(h-self.y))
			print("#########")
			print((1/(self.x.shape[0]))*((h-self.y).T.dot(self.x)))
		print(self.theta)
		print(self.alpha_history)
		print(self.cost_history)
