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











