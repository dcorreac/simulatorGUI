from tkinter import *


root = Tk() # initialize Tkinter

myTextWidget= Text(root) # set up a text widget as a root (window) child

myFile = open("out.txt") # get a file handle
myText= myFile.read() # read the file to variable
myFile.close() # close file handle

myTextWidget.insert(0.0,myText) # insert the file's text into the text widget

myTextWidget.pack(expand=1, fill=BOTH) # show the widget

root.mainloop() #run the events mainloop
# End the example here