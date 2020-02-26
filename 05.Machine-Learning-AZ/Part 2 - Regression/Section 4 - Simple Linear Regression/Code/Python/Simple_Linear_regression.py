
# importing libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as pt
pt.rcParams["backend"] = "TkAgg"

# importing dataset
dataset = pd.read_csv('../../Simple_Linear_Regression/Salary_Data.csv')
x = dataset.iloc[:, :-1]
y = dataset.iloc[:, -1]
"""
# Taking care of missing data
from sklearn.impute import SimpleImputer
impute = SimpleImputer(missing_values=np.nan, strategy='mean')
impute = impute.fit(x.iloc[:, 1:3])
x.iloc[:, 1:3] = impute.transform(x.iloc[:, 1:3])
"""

"""
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
encoder = LabelEncoder()
x.iloc[:, 0] = encoder.fit_transform(x.iloc[:, 0])
# hotencoder = OneHotEncoder(categorical_features = [0])
# n = hotencoder.fit_transform(x).toarray()
# print(n)
encoder = LabelEncoder()
y = encoder.fit_transform(y)
"""

from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=0)
"""
from sklearn.preprocessing import StandardScaler
sc_x = StandardScaler()
x_train = sc_x.fit_transform(x_train)
x_test = sc_x.transform(x_test)
print(x_test)
"""

from sklearn.linear_model import LinearRegression
regresor = LinearRegression()
regresor.fit(x_train, y_train)

y_pred = regresor.predict(x_test)

pt.scatter(x_test, y_test)
pt.plot(x_test, y_pred)
pt.title("Experience VS Salary")
pt.show()