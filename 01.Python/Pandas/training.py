import numpy as np
import pandas as pd

series = np.array([23,23,23,23,4])
seri = pd.Series(series)
print(seri)

a = {'a':23,'v':22,'s':44}
print(pd.Series(a))

b = np.arange(12).reshape(4,3)
print(pd.DataFrame(b,index=["age","age1","age2","ds"]))

c = np.arange(12).reshape(2,2,3)
print(pd.Panel(c))
