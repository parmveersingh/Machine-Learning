
# importing libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as pt

# importing dataset
dataset = pd.read_csv('../../Data-Preprocessing/Data.csv')
x = dataset.iloc[:, :-1]
y = dataset.iloc[:, -1]

# Taking care of missing data
from sklearn.impute import SimpleImputer
impute = SimpleImputer(missing_values=np.nan, strategy='mean')
impute = impute.fit(x.iloc[:, 1:3])
x.iloc[:, 1:3] = impute.transform(x.iloc[:, 1:3])

from sklearn.preprocessing import LabelEncoder
encoder = LabelEncoder()
x.iloc[:, 0] = encoder.fit_transform(x.iloc[:, 0])
print(x)