import numpy as np
import numpy.matlib

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

#make array of row with arrange

print(np.arange(23))

#use reshape on arrage

arraj = np.arange(24)
print(arraj.reshape(2,3,4))

# array with empty values, 1's and with 0's

print(np.empty([2,3],dtype=int))
print(np.zeros([3,3],dtype=int))
print(np.ones([2,3],dtype=int))

# for creating anything as array

x= (1,3,54,3)
print(np.asarray(x,dtype=float))

print(np.frombuffer(arr,dtype=float))

# for getting in between values

print(np.arange(1,10,2))

print(np.linspace(1,23,24))


### SLICING AND INDEXING ####


a= np.arange(24)
print(a[1:8])

b = np.empty([3,4],dtype=int)
print(b[...,1:])

# advance slicing 

print(b[[1,2],1:4])

#addition of 2 unequal arrays 

a = np.array([[0.0,0.0,0.0],[10.0,10.0,10.0],[20.0,20.0,20.0],[30.0,30.0,30.0]]) 
b = np.array([1.0,2.0,3.0])

print a+b

# loop in arrays

for x in np.nditer(a):
	print x


###### ARRAY MANIPULATION #####

# shape changing

print(a.reshape(3,4))

print(a.flat[5])

print(a.flatten())

# transpose

print(np.transpose(a))

print(a.T)


# Joining arrays

c = a.flatten()
d = np.array(b,ndmin=2)
print(d)
print(np.concatenate([c,b]))

print(np.hstack([c,b]))


# split arrays

print(np.split(a,4))

## hsplit and vsplit was there with this



############# STRING FUNCTIONS #############


e = np.array([['dsd','asd','sdfsdf']])
f = np.array([['gh','dd','ccv']])
print(np.char.add(e,f))

# many more functions are like this add,multiply,center,capitalize,title,upper,lower,split,strip,join,replace,decode,encode


############ Mathematical Functions ##########

a = np.array([0,30,45])
sinh=np.sin(a*np.pi/180)
print(sinh)

inv = np.arcsin(sinh)
print inv

print(np.degrees(inv))

# more functions like around, floor and ceil

# more function add,subtract,multiple,divide,remainder,reciprocal,power

# more functions are available like amin, amax, percentile, median, mean, average and standard deviation

### test my knowledge ###
z = np.arange(24,dtype='int').reshape(12,2)
print(z[:,0])

# sort and search 

a = np.array([[23,43,5,34,23,12],[23,23,45,1,34,5]])
print(np.sort(a))

print(np.argsort(a))

print(np.lexsort(a))

print(np.argmax(a))

print(np.argmin(a))

print(np.nonzero(a))

print(np.where(x==12))

# extract is for getting element that satisfy condition


# copy a array

## there are 3 types of copy of arrays

#1 a=b, in which changes made to b is also shown in a because both have same id like in c
#2 b= a.view(), in which id's are different
#3 c= a.copy(), this create completely different array.


### Matrix in numpy

print(np.matlib.empty([2,4]))

print(np.matlib.zeros([3,2]))
print(np.matlib.ones([3,2]))
print(np.matlib.eye(3,2,0))
print(np.matlib.identity(4))

print(np.matlib.rand(2,2))

print(np.asmatrix(a))

### Linear Algebra

# dot product of arrays
b = np.array([[3,3],[15,4],[23,32],[23,23],[5,21],[34,5]])
print(np.dot(a,b))

# there is vdot product is also available

# inner product of array is also we can do

a = np.array([[1,2], [3,4]])
b = np.array([[11, 12], [13, 14]]) 
print np.inner(a,b)

## there is one more function for matrix multiplication that is matmul


################### MOST IMPORTANT CODE OF DETERMINANT ##################


print(np.linalg.det(a))


# FOR SOLVING LINEAR EXUATION WE HAVE

a = np.array([[3,1], [1,2]])
b = np.array([9,8])
print(np.linalg.solve(a, b))


# for inverse we have method 

print(np.linalg.inv(a))

## Save and load numpy array

np.save('check',a)

y = np.load('check.npy')
print(y)


### to save in text file we have savetxt and loadtxt function

