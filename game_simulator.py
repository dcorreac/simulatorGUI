import pandas
import numpy
import requests
import bs4
import nose.tools
import random 
from statistics import mean



def game_simulator(team1, team2):  
    file = open('out.txt', 'w')
    team1score = 0 
    team2score = 0 
    url = 'https://www.sports-reference.com/cbb/schools/' +team1 + '/2020.html#all_per_game'
    page = requests.get(url)
    f = open('downloaded.html','w', encoding = "utf-8")
    f.write(page.text)
    soup = bs4.BeautifulSoup(open("downloaded.html"), 'html.parser')
    SRS1 =int((str(soup.find_all('p')[6]).split("/strong>")[1].split("(")[1].replace("st", " ").replace("nd", " ").replace("rd", " ").replace("th", " ")).split()[0])
    tables = soup.find_all('table')
    table = tables[2]
    
    teamTable1 = tables[1]
    rows = teamTable1.find_all('tr')
    
    defense1 = []    
    i = 0
    
    for row in rows:
        j = 0
        columns = row.find_all('td')
        row = []
        for column in columns:
            text = column.string
            row.append(text)
        defense1.append(row)
    defence1 = pandas.DataFrame(defense1, columns = ['G', 'MP', 'FG', 'FGA','FG%', '2P', '2PA', '2P%', '3P', '3PA', '3P%', 'FT','FTA', 'FT%','ORB','DRB', 'TRB', 'AST', 'STL','BLK','TOV', 'PF','PTS', 'PTS/G'])    
    
    
    
    
    
    SRSmax = 353
    
    
    
    
    
    rows = table.find_all('tr')
    data = [] 
    i = 0
    for row in rows:
        j = 0
        columns = row.find_all('td')
        row = []
        for column in columns:
            text = column.string
            row.append(text)
        data.append(row)
    data = pandas.DataFrame(data, columns = ["Name", "G", "GS", "MP", "FG", "FGA", "FG%", "2P","2PA", "2P%", "3P", "3PA", "3P%", "FT", 'FTA', 'FT%', 'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS'])
    data = data.iloc[1:]
    

    for column in data.columns: 
        if column != "Name":
            data[column] = pandas.to_numeric(data[column])
    boxScore = pandas.DataFrame(columns = ['Name', 'Points', '2PM', '2PA', '3PM', '3PA', 'TOV', "ORB", "DRB", "TRB"])
    boxScore['Name'] = data['Name']
    boxScore = boxScore.fillna(0)

    url = 'https://www.sports-reference.com/cbb/schools/' +team2 + '/2020.html#all_per_game'
    page = requests.get(url)
    f = open('downloaded.html','w', encoding = "utf-8")
    f.write(page.text)
    soup = bs4.BeautifulSoup(open("downloaded.html"), 'html.parser')
    SRS2 =int((str(soup.find_all('p')[6]).split("/strong>")[1].split("(")[1].replace("st", " ").replace("nd", " ").replace("rd", " ").replace("th", " ")).split()[0] )
    tables = soup.find_all('table')
    
    teamTable2 = tables[1]
    rows = teamTable2.find_all('tr')
    
    defense2 = []    
    i = 0
    for row in rows:
        j = 0
        columns = row.find_all('td')
        row = []
        for column in columns:
            text = column.string
            row.append(text)
        defense2.append(row)
    defence2 = pandas.DataFrame(defense2, columns = ['G', 'MP', 'FG', 'FGA','FG%', '2P', '2PA', '2P%', '3P', '3PA', '3P%', 'FT','FTA', 'FT%','ORB','DRB', 'TRB', 'AST', 'STL','BLK','TOV', 'PF','PTS', 'PTS/G'])    

    
    
    table = tables[2]
    rows = table.find_all('tr')
    data2 = [] 
    i = 0
    for row in rows:
        j = 0
        columns = row.find_all('td')
        row = []
        for column in columns:
            text = column.string
            row.append(text)
        data2.append(row)
    data2 = pandas.DataFrame(data2, columns = ["Name", "G", "GS", "MP", "FG", "FGA", "FG%", "2P","2PA", "2P%", "3P", "3PA", "3P%", "FT", 'FTA', 'FT%', 'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS'])
    data2 = data2.iloc[1:]
    

    for column in data2.columns: 
        if column != "Name":
            data2[column] = pandas.to_numeric(data2[column])
    boxScore2 = pandas.DataFrame(columns = ['Name', 'Points', '2PM', '2PA', '3PM', '3PA', 'TOV',"ORB", "DRB", "TRB"])
    boxScore2['Name'] = data2['Name']
    boxScore2 = boxScore2.fillna(0)


    SRScoeff1 = .2+ (.8*((SRSmax-SRS1)/(SRSmax-1)))
    SRScoeff2 = .2 + (.8*((SRSmax-SRS2)/(SRSmax-1)))
    
    

    for ghe in range(0,1):
        time = 50*60 
        score1 = 0
        score2 = 0 
        turnovers1 = 0
        turnovers2 = 0 
        pos = 1
        while time > 0: 
            if(pos == 1):
                
                FGA = data.FGA.sum()
                TOV = data.TOV.sum()
                FGA2 = data["2PA"].sum()
                FGM2 = data["2P"].sum()
                FGA3 = data["3PA"].sum()
                FGM3 = data["3P"].sum()
                Drebound = data2["DRB"].sum()*SRScoeff2
                Orebound = data["ORB"].sum()*SRScoeff1
                oppTeamTOV = float(defence2.loc[3, "TOV"])/float(defence2.loc[3, "G"])  #TOV/G other team forces
                oppDTeam2PA = float(defence2.loc[3, "2PA"])/float(defence2.loc[3, "G"]) #2PA/G other team allows
                oppDTeam3PA = float(defence2.loc[3, "3PA"])/float(defence2.loc[3, "G"]) #3PA/G other team allows 
                oppDTeam2Per = float(defence2.loc[3, "2P%"])
                oppDTeam3Per = float(defence2.loc[3, "3P%"])
                
                
    
                
                cof1 = 100* (FGA/(FGA+(TOV+oppTeamTOV)/2)) #percent of possesions that result in shot attempt. 
                rand1 = random.randint(1,101) 
                if(cof1 >= rand1):
                    cof2 = 100*((FGA2 + oppDTeam2PA)/(FGA2 + FGA3+ oppDTeam2PA + oppDTeam3PA)) #percent of shot attempts that are 2 point FG
                    rand2 = random.randint(1,101) 
                    if(cof2  >= rand2):
                        cof3 = SRScoeff1*100*((FGM2/(FGA2)) + oppDTeam2Per)/2 #percent of 2PT FG that go in 
                        rand3 = random.randint(1,101)
                        if(cof3 >= rand3): #Checking if 2PT FG is missed 
                            picked = 0 
                            while picked == 0: #Picking 2PT FG maker
                                rand4 = random.randint(1,data.shape[0]-1) 
                                rand5 = random.randint(1,101)
                                cof4 = 100 *(data.loc[rand4, "2P"]/FGM2)
                                if(cof4 >= rand5):
                                    picked = 1
                                    file.write(str("2PT FG by " + data.loc[rand4, "Name"])+  "\n")
                                    boxScore.at[rand4, "2PM"] = boxScore.loc[rand4, "2PM"] + 1
                                    boxScore.at[rand4, "2PA"] = boxScore.loc[rand4, "2PA"] + 1
                                    boxScore.at[rand4, "Points"] = boxScore.loc[rand4, "Points"] + 2
                                    score1 = score1 + 2
                                    pos = 2

                        else:
                            picked = 0 
                            while picked == 0: #Picking 2PT FG misser
                                rand4 = random.randint(1,data.shape[0]-1) 
                                rand5 = random.randint(1,101)
                                cof4 = 100 *((data.loc[rand4, "2PA"] - data.loc[rand4, "2P"])/(FGA2- FGM2))
                                if(cof4 >= rand5):
                                    picked = 1
                                    file.write(str("2PT FG missed by " + data.loc[rand4, "Name"])+  "\n")
                                    boxScore.at[rand4, "2PA"] = boxScore.loc[rand4, "2PA"] + 1
                                    offRebound = 100 *(Orebound/(Drebound + Orebound)) #offensive rebounding rate for team 
                                    randomRebound = random.randint(1,101)
                                    if(offRebound >= randomRebound):
                                        pos = 1
                                        picked = 0 
                                        while picked == 0: #Picking offensive rebounder
                                            rand4 = random.randint(1,data.shape[0]-1) 
                                            rand5 = random.randint(1,101)
                                            cof4 = 100 *(data.loc[rand4, "ORB"]/Orebound)
                                            if(cof4 >= rand5):
                                                picked = 1
                                                file.write(str("Offensive rebound by " + data.loc[rand4, "Name"])+  "\n")
                                                boxScore.at[rand4, "ORB"] = boxScore.loc[rand4, "ORB"] + 1
                                                boxScore.at[rand4, "TRB"] = boxScore.loc[rand4, "TRB"] + 1

                                    else: #picking defensive rebounder for opposing team
                                        pos = 2
                                        picked = 0 
                                        while picked == 0: #Picking defensive rebounder for the opposing team 
                                            rand4 = random.randint(1,data2.shape[0]-1) 
                                            rand5 = random.randint(1,101)
                                            cof4 = 100 *(data2.loc[rand4, "DRB"]/Drebound)
                                            if(cof4 >= rand5):
                                                picked = 1
                                                file.write(str("Defensive rebound by " + data2.loc[rand4, "Name"])+  "\n")
                                                boxScore2.at[rand4, "DRB"] = boxScore2.loc[rand4, "DRB"] + 1
                                                boxScore2.at[rand4, "TRB"] = boxScore2.loc[rand4, "TRB"] + 1



                    else:
                        cof6 = SRScoeff1*100*((FGM3/(FGA3)) + oppDTeam3Per)/2 #percent of 3PT FG that go in 
                        rand6 = random.randint(1,101)
                        if(cof6 >= rand6): #Checking if 3PT FG is missed 
                            picked2 = 0 
                            while picked2 == 0: #Picking 3PT FG maker
                                rand4 = random.randint(1,data.shape[0]-1) 
                                rand5 = random.randint(1,101)
                                cof4 = 100 *(data.loc[rand4, "3P"]/FGM3)
                                if(cof4 >= rand5):
                                    picked2 = 1
                                    file.write(str("3PT FG by " + data.loc[rand4, "Name"])+  "\n")
                                    boxScore.at[rand4, "3PM"] = boxScore.loc[rand4, "3PM"] + 1
                                    boxScore.at[rand4, "3PA"] = boxScore.loc[rand4, "3PA"] + 1
                                    boxScore.at[rand4, "Points"] = boxScore.loc[rand4, "Points"] + 3
                                    score1 = score1 + 3
                                    pos = 2
                        else:
                            picked = 0 
                            while picked == 0: #Picking 3PT FG misser
                                rand4 = random.randint(1,data.shape[0]-1) 
                                rand5 = random.randint(1,101)
                                cof4 = 100 *((data.loc[rand4, "3PA"] - data.loc[rand4, "3P"])/(FGA3- FGM3))

                                if(cof4 >= rand5):
                                    picked = 1
                                    file.write(str("3PT FG missed by " + data.loc[rand4, "Name"])+  "\n")
                                    boxScore.at[rand4, "3PA"] = boxScore.loc[rand4, "3PA"] + 1
                                    offRebound = 100 *(Orebound/(Drebound + Orebound)) #offensive rebounding rate for team 
                                    randomRebound = random.randint(1,101)
                                    if(offRebound >= randomRebound):
                                        pos = 1
                                        picked = 0 
                                        while picked == 0: #Picking offensive rebounder
                                            rand4 = random.randint(1,data.shape[0]-1) 
                                            rand5 = random.randint(1,101)
                                            cof4 = 100 *(data.loc[rand4, "ORB"]/Orebound)
                                            if(cof4 >= rand5):
                                                picked = 1
                                                file.write(str("Offensive rebound by " + data.loc[rand4, "Name"])+  "\n")
                                                boxScore.at[rand4, "ORB"] = boxScore.loc[rand4, "ORB"] + 1
                                                boxScore.at[rand4, "TRB"] = boxScore.loc[rand4, "TRB"] + 1

                                    else: #picking defensive rebounder for opposing team
                                        pos = 2
                                        picked = 0 
                                        while picked == 0: #Picking defensive rebounder for the opposing team 
                                            rand4 = random.randint(1,data2.shape[0]-1) 
                                            rand5 = random.randint(1,101)
                                            cof4 = 100 *(data2.loc[rand4, "DRB"]/Drebound)
                                            if(cof4 >= rand5):
                                                picked = 1
                                                file.write(str("Defensive rebound by " + data2.loc[rand4, "Name"])+  "\n")
                                                boxScore2.at[rand4, "DRB"] = boxScore2.loc[rand4, "DRB"] + 1
                                                boxScore2.at[rand4, "TRB"] = boxScore2.loc[rand4, "TRB"] + 1


                else:
                    picked3 = 0 
                    while picked3 == 0:
                        rand4 = random.randint(1,data.shape[0]-1) 
                        rand5 = random.randint(1,101)
                        cof4 = 100 *(data.loc[rand4, "TOV"]/TOV)
                        if(cof4 >= rand5):
                            picked3 = 1
                            turnovers1 = turnovers1 + 1
                            file.write(str("Turnover by " + data.loc[rand4, "Name"])+  "\n")
                            boxScore.at[rand4, "TOV"] = boxScore.loc[rand4, "TOV"] + 1
                            pos = 2
            time = time - 15
            if(pos == 2):
                FGAb = data2.FGA.sum()
                TOVb = data2.TOV.sum()
                FGA2b = data2["2PA"].sum()
                FGM2b = data2["2P"].sum()
                FGA3b = data2["3PA"].sum()
                FGM3b = data2["3P"].sum()
                Drebound = data["DRB"].sum()*SRScoeff1
                Orebound = data2["ORB"].sum()*SRScoeff2
                oppTeamTOV = float(defence1.loc[3, "TOV"])/float(defence1.loc[3, "G"])
                oppDTeam2PA = float(defence1.loc[3, "2PA"])/float(defence1.loc[3, "G"]) #2PA/G other team allows
                oppDTeam3PA = float(defence1.loc[3, "3PA"])/float(defence1.loc[3, "G"]) #3PA/G other team allows
                oppDTeam2Per = float(defence1.loc[3, "2P%"])
                oppDTeam3Per = float(defence1.loc[3, "3P%"])
                cof1 = 100* (FGA/(FGA+(TOV+oppTeamTOV)/2)) #percent of possesions that result in shot attempt. 
                rand1 = random.randint(1,101) 
                if(cof1 >= rand1):
                    cof2 = 100*((FGA2 + oppDTeam2PA)/(FGA2 + FGA3+ oppDTeam2PA + oppDTeam3PA)) #percent of shot attempts that are 2 point FG
                    rand2 = random.randint(1,101) 
                    if(cof2  >= rand2):
                        cof3 = SRScoeff2*100*((FGM2/(FGA2)) + oppDTeam2Per)/2 #percent of 2PT FG that go in 
                        rand3 = random.randint(1,101)
                        if(cof3 >= rand3): #Checking if 2PT FG is missed 
                            picked = 0 
                            while picked == 0: #Picking 2PT FG maker
                                rand4 = random.randint(1,data2.shape[0]-1) 
                                rand5 = random.randint(1,101)
                                cof4 = 100 *(data2.loc[rand4, "2P"]/FGM2b)
                                if(cof4 >= rand5):
                                    picked = 1
                                    file.write(str("2PT FG by " + data2.loc[rand4, "Name"])+  "\n")
                                    boxScore2.at[rand4, "2PM"] = boxScore2.loc[rand4, "2PM"] + 1
                                    boxScore2.at[rand4, "2PA"] = boxScore2.loc[rand4, "2PA"] + 1
                                    boxScore2.at[rand4, "Points"] = boxScore2.loc[rand4, "Points"] + 2
                                    score2 = score2 + 2
                                    pos = 1 

                        else:
                            picked = 0 
                            while picked == 0: #Picking 2PT FG misser
                                rand4 = random.randint(1,data2.shape[0]-1) 
                                rand5 = random.randint(1,101)
                                cof4 = 100 *((data2.loc[rand4, "2PA"] - data2.loc[rand4, "2P"])/(FGA2b- FGM2b))
                                if(cof4 >= rand5):
                                    picked = 1
                                    file.write(str("2PT FG missed by " + data2.loc[rand4, "Name"])+  "\n")
                                    boxScore2.at[rand4, "2PA"] = boxScore2.loc[rand4, "2PA"] + 1
                                    offRebound = 100 *(Orebound/(Drebound + Orebound)) #offensive rebounding rate for team 
                                    randomRebound = random.randint(1,101)
                                    if(offRebound >= randomRebound):
                                        pos = 2
                                        picked = 0 
                                        while picked == 0: #Picking offensive rebounder
                                            rand4 = random.randint(1,data2.shape[0]-1) 
                                            rand5 = random.randint(1,101)
                                            cof4 = 100 *(data2.loc[rand4, "ORB"]/Orebound)
                                            if(cof4 >= rand5):
                                                picked = 1
                                                file.write(str("Offensive rebound by " + data2.loc[rand4, "Name"])+  "\n")
                                                boxScore2.at[rand4, "ORB"] = boxScore2.loc[rand4, "ORB"] + 1
                                                boxScore2.at[rand4, "TRB"] = boxScore2.loc[rand4, "TRB"] + 1

                                    else: #picking defensive rebounder for opposing team
                                        pos = 1
                                        picked = 0 
                                        while picked == 0: #Picking defensive rebounder for the opposing team 
                                            rand4 = random.randint(1,data.shape[0]-1) 
                                            rand5 = random.randint(1,101)
                                            cof4 = 100 *(data.loc[rand4, "DRB"]/Drebound)
                                            if(cof4 >= rand5):
                                                picked = 1
                                                file.write(str("Defensive rebound by " + data.loc[rand4, "Name"])+  "\n")
                                                boxScore.at[rand4, "DRB"] = boxScore.loc[rand4, "DRB"] + 1
                                                boxScore.at[rand4, "TRB"] = boxScore.loc[rand4, "TRB"] + 1



                    else:
                        cof6 = SRScoeff2*100*((FGM3/(FGA3)) + oppDTeam3Per)/2 #percent of 3PT FG that go in 
                        rand6 = random.randint(1,101)
                        if(cof6 >= rand6): #Checking if 3PT FG is missed 
                            picked2 = 0 
                            while picked2 == 0: #Picking 3PT FG maker
                                rand4 = random.randint(1,data2.shape[0]-1) 
                                rand5 = random.randint(1,101)
                                cof4 = 100 *(data2.loc[rand4, "3P"]/FGM3b)
                                if(cof4 >= rand5):
                                    picked2 = 1
                                    file.write(str("3PT FG by " + data2.loc[rand4, "Name"])+  "\n")
                                    boxScore2.at[rand4, "3PM"] = boxScore2.loc[rand4, "3PM"] + 1
                                    boxScore2.at[rand4, "3PA"] = boxScore2.loc[rand4, "3PA"] + 1
                                    boxScore2.at[rand4, "Points"] = boxScore2.loc[rand4, "Points"] + 3
                                    score2 = score2 + 3
                                    pos = 1 
                        else:
                            picked = 0 
                            while picked == 0: #Picking 3PT FG misser
                                rand4 = random.randint(1,data2.shape[0]-1) 
                                rand5 = random.randint(1,101)
                                cof4 = 100 *((data2.loc[rand4, "3PA"] - data2.loc[rand4, "3P"])/(FGA3b- FGM3b))

                                if(cof4 >= rand5):
                                    picked = 1
                                    file.write(str("3PT FG missed by " + data2.loc[rand4, "Name"])+  "\n")
                                    boxScore2.at[rand4, "3PA"] = boxScore2.loc[rand4, "3PA"] + 1
                                    offRebound = 100 *(Orebound/(Drebound + Orebound)) #offensive rebounding rate for team 
                                    randomRebound = random.randint(1,101)
                                    if(offRebound >= randomRebound):
                                        pos = 2
                                        picked = 0 
                                        while picked == 0: #Picking offensive rebounder
                                            rand4 = random.randint(1,data2.shape[0]-1) 
                                            rand5 = random.randint(1,101)
                                            cof4 = 100 *(data2.loc[rand4, "ORB"]/Orebound)
                                            if(cof4 >= rand5):
                                                picked = 1
                                                file.write(str("Offensive rebound by " + data2.loc[rand4, "Name"])+  "\n")
                                                boxScore2.at[rand4, "ORB"] = boxScore2.loc[rand4, "ORB"] + 1
                                                boxScore2.at[rand4, "TRB"] = boxScore2.loc[rand4, "TRB"] + 1

                                    else: #picking defensive rebounder for opposing team
                                        pos = 1
                                        picked = 0 
                                        while picked == 0: #Picking defensive rebounder for the opposing team 
                                            rand4 = random.randint(1,data.shape[0]-1) 
                                            rand5 = random.randint(1,101)
                                            cof4 = 100 *(data.loc[rand4, "DRB"]/Drebound)
                                            if(cof4 >= rand5):
                                                picked = 1
                                                file.write(str("Defensive rebound by " + data.loc[rand4, "Name"])+  "\n")
                                                boxScore.at[rand4, "DRB"] = boxScore.loc[rand4, "DRB"] + 1
                                                boxScore.at[rand4, "TRB"] = boxScore.loc[rand4, "TRB"] + 1



                else:
                    picked3 = 0 
                    while picked3 == 0:
                        rand4 = random.randint(1,data2.shape[0]-1) 
                        rand5 = random.randint(1,101)
                        cof4 = 100 *(data2.loc[rand4, "TOV"]/TOVb)
                        if(cof4 >= rand5):
                            picked3 = 1
                            turnovers2 = turnovers2 + 1
                            file.write(str("Turnover by " + data2.loc[rand4, "Name"])+  "\n")
                            boxScore2.at[rand4, "TOV"] = boxScore2.loc[rand4, "TOV"] + 1
                            pos = 1


            file.write(str("Time left: " + str(time/60) + "------ Score: " + str(score1) + " to " + str(score2))+  "\n")    
            time = time - 15 
            if(time <= 0 and (score1 == score2)):
                time == time + 5
        
        
        if(score1 >= score2):
            return team1
        else:
            return team2

        file.write(team1+ ": " + str(score1)+  "\n")
        file.write(team2+ ": " +str(score2)+  "\n")
        file.write(str(boxScore)+  "\n")
        file.write(str(boxScore2)+  "\n")
        file.close()
