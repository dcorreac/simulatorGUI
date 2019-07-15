from tkinter import *
from game_simulator import game_simulator



root = Tk()

Label(root, text = "Team 1").grid(row = 0, sticky = W)
Label(root, text = "Team 2").grid(row = 1, sticky = W)


team1 = Entry(root)
team2 = Entry(root)



team1.grid(row = 0, column = 1)
team2.grid(row = 1, column = 1)


def getInput():

    a = team1.get()
    b = team2.get()
    game_simulator(a,b)
    

    global params
    params = [a,b]


Button(root, text = "submit",
           command = getInput).grid(row = 5, sticky = W)


root.mainloop()

