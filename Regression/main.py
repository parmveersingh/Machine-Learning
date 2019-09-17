import numpy as np
import pandas as pd
import matplotlib.pyplot as mp


# Read csv file
data=pd.read_csv("salary_data.csv")
print(data)

# plot a dots on graph

mp.scatter(data.iloc[:,0:1].values,data.iloc[:,1].values)
mp.xlabel('Years of Experience')
mp.ylabel('Salary')
mp.title('Salary Based on Experience')
#mp.show()


# Shuffle a data 

data = data.sample(frac=1)
x=data.iloc[:,0].values
y=data.iloc[:,1].values


from FeatureScaling import FeatureScaling
fs=FeatureScaling(x,y)
fs_x=fs.fit_scaling_X()
print(fs_x)


