import numpy as np
import pandas as pd
import matplotlib.pyplot as mp


# Read csv file
data=pd.read_csv("Startups.csv")
print(data)

feature_count=data.shape[1]-1

# plot a dots on graph
'''
mp.scatter(data.iloc[:,:feature_count].values,data.iloc[:,feature_count].values)
mp.xlabel('Years of Experience')
mp.ylabel('Salary')
mp.title('Salary Based on Experience')
#mp.show() '''


# Shuffle a data 

data = data.sample(frac=1)
x=data.iloc[:,:(feature_count-1)].values
y=data.iloc[:,feature_count].values
exp_y=y[int(y.size*0.7):]


# feature scaling, so that both the features are at same scale
from FeatureScaling import FeatureScaling
fs=FeatureScaling(x,y)
fs_x=fs.fit_scaling_X()
fs_y=fs.fit_scaling_Y()

	
# split into training and testing examples
train_x=fs_x[0:int(fs_x.shape[0]*0.7),:]
train_y=fs_y[:int(fs_y.size*0.7),:]

test_x=fs_x[int(fs_x.shape[0]*0.7):,:]
test_y=fs_y[int(fs_y.size*0.7):,:]

# linear regression execution
from linear_regression import LinearRegression
ls = LinearRegression(train_x,train_y)
j=ls.cost_function()


iters=1000
alpha=0.07

theta,cost_history,theta_history=ls.gradient(iters,alpha)
y_pred,error_pred=ls.predict(test_x,theta,test_y)
y_pred=fs.inverse_fit_scaling_Y(y_pred)
print(pd.DataFrame(np.vstack([exp_y,y_pred[:,0]]),index=["Actual Values",'Predicted Values']).T)
