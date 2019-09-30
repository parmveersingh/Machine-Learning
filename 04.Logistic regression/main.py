import numpy as np
import pandas as pd
import matplotlib.pyplot as mp

data= pd.read_csv("plants_data.csv")

data=data.replace({"Iris-setossa":"Iris-setosa","versicolor":"Iris-versicolor"})
data= data.dropna(subset=['petal_width_cm'])

data= data[data["classes"] != "Iris-versicolor"]
data=data.replace({"Iris-setosa":0,"Iris-virginica":1})

data= data.sample(frac=1)

last_feature_index= data.shape[1]-1
x_axis= data.iloc[:,:last_feature_index].values
y_axis= data.iloc[:,last_feature_index].values

from feature_scaling import Feature_Scaling

fs = Feature_Scaling(x_axis,y_axis)
fs_x = fs.feature_x()
fs_y = fs.feature_y()


train_x= fs_x[:int(fs_x.shape[0]*0.7),:]
train_y= fs_y[:int(fs_y.shape[0]*0.7)]

test_x= fs_x[int(fs_x.shape[0]*0.7):,:]
test_y= fs_y[int(fs_y.shape[0]*0.7):]


from logistic_regression import Logistic_Regression

lr = Logistic_Regression(train_x,train_y)
lr.equation()
lr.cost_function()
alpha=0.05
iters=2000
theta=lr.gradient(iters,alpha)
pred_y=lr.pred(theta,test_x,test_y)
pred_y=fs.rev_feature_y(pred_y)
change_pred_y=pred_y-np.min(pred_y)
mean_pred_y=np.mean(pred_y-np.min(pred_y))
pred_y=np.where(change_pred_y<mean_pred_y,0,1)
print(pd.DataFrame(np.vstack([test_y,np.around(pred_y)]),index=["Actual Values",'Predicted Values']).T) 


