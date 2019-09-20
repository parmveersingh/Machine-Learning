import numpy as np
import pandas as pd
import matplotlib.pyplot as mp


# Read csv file
data=pd.read_csv("salary_data.csv")
print(data)

# plot a dots on graph

mp.scatter(data.iloc[:,:1].values,data.iloc[:,1].values)
mp.xlabel('Years of Experience')
mp.ylabel('Salary')
mp.title('Salary Based on Experience')
#mp.show()


# Shuffle a data 

data = data.sample(frac=1)
x=data.iloc[:,:1].values
y=data.iloc[:,1].values

# feature scaling, so that both the features are at same scale
from FeatureScaling import FeatureScaling
fs=FeatureScaling(x,y)
fs_x=fs.fit_scaling_X()
fs_y=fs.fit_scaling_Y()


train_x=fs_x[:int(fs_x.size*0.7),:]
train_y=fs_y[:int(fs_y.size*0.7),:]

test_x=fs_x[int(fs_x.size*0.7):,:]
test_y=fs_y[int(fs_y.size*0.7):,:]

from linear_regression import LinearRegression
ls = LinearRegression(train_x,train_y)
ls.cost_function()

iters=1000
alpha=0.05

#ls.gradient(iters,alpha)


