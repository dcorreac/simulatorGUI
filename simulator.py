from tkinter import *
from game_simulator import game_simulator



root = Tk()

Label(root, text = "Team 1:").grid(row = 0, sticky = W)
Label(root, text = "Team 2:").grid(row = 1, sticky = W)


team1 = Entry(root)
team2 = Entry(root)



team1.grid(row = 0, column = 1)
team2.grid(row = 1, column = 1)


def getInput():

    a = team1.get()
    b = team2.get()
    game_simulator(a,b)
    
    
    myTextWidget= Text(root) # set up a text widget as a root (window) child

    myFile = open("out.txt") # get a file handle
    myText= myFile.read() # read the file to variable
    myFile.close() # close file handle

    myTextWidget.insert(0.0,myText) # insert the file's text into the text widget

    #myTextWidget.pack(expand=1, fill=BOTH) # show the widget

    myTextWidget.grid(row = 7, column = 1)



Button(root, text = "simulate",
           command = getInput).grid(row = 5, sticky = W)






root.mainloop()

