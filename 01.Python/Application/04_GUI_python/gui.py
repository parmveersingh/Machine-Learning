from Tkinter import *

window = Tk()

b1 = tkButtonDown()
b1.grid(row=0,column=1)

e1 = Entry(window)
e1.grid(row=0,column=2)

t1 = Text(window,height=1,width=30)
t1.grid(row=0,column=3)

window.mainloop()
