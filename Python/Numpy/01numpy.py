import numpy as np

# creating a simple array

arr = np.array([[1,32,32],[1,34,52]])
print(arr)

#checking type of numpy

print("type of arr "+str(type(arr)))

# ndmin using

arry = np.array([1,32,4,43,23],ndmin=3) 
print(arry)

# dtype in array

arrys = np.array([2,43,23,12],dtype=complex)
print(arrys)


# giving datatype to numpy arrays

student = np.dtype([('name','S20'),('age','i1'),('marks','f4')])
ar = np.array([('wsd',12,23.4),('sd',23,23.44)],dtype=student)
print(ar)


##### ARRAY ATTRIBUTES #######
print("##### ARRAY ATTRIBUTES #######")

# shape

print(ar.shape)
print(arr.shape)

# change shape of array with use of shape

arr.shape=(3,2)
print(arr)

# reshape an arr

print(arrys.reshape(2,2))
