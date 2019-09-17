import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class LinearRegression:
	
	def __init__(self,x,y):
		ones=np.ones([x.shape[0],1],dtype=int)
		self.x=np.append(x,ones,axis=1)
		self.y=y
		self.theta=np.random.randn(x.shape[1])


	def return_theta(self):
	
		return self.theta


	def cost_function(self):

		h=np.matmul(self.x,self.theta)
		print(h)

