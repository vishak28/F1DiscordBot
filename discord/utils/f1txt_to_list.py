import pandas as pd


standings = pd.read_csv("./database/winners.txt", sep = "\t",encoding='latin-1')
standings.drop(['NO','CAR','LAPS','TIME/RETIRED','PTS'], inplace=True,axis=1)

#creating a winners dictionary to store their name as th key and their position as value
winnersDict = {}
for index in standings.index:
    if standings['POS'][index] == 'NC':
        result = '20'
    else:
        result = standings['POS'][index]
    winnersDict[standings['DRIVER'][index]] = result

#Bwoah, Kimi's last name fucks up the encoding
winnersDict['Kimi Räikkönen'] = winnersDict.pop('Kimi RÃ¤ikkÃ¶nen')
print(winnersDict)