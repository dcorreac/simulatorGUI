# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 19:47:31 2019

@author: dan
"""

from game_simulator import game_simulator 

def game_assamble(team1, team2):
    
    team1_tally = 0 
    team2_tally = 0
    for i in range(0,100):
        won = game_simulator(team1,team2)
        if(won == team1):
            team1_tally = team1_tally + 1
        if(won == team2):
            team2_tally = team2_tally + 1
    
    file = open('out2.txt', 'w')     
    odds1 = team1_tally/1
    odds2 = team2_tally/1
    file.write(team1 + ": " + str(odds1) + "% chance of winning\n")
    file.write(team2 + ": " + str(odds2) + "% chance of winning")
    file.close()
    