import pandas as pd
import numpy as np
import math as m
import func as f
import os.path

homedir = os.path.expanduser("~") #to open the file from another computer

player = input('Enter a player name: ')
team = input('Enter a team that they played for (3 letter acronym): ') #speeds up name search by a million and eliminates 2 player same name issue
season = int(input('Enter a season (1993-2018): '))

#following if statements determine which file to open
#this is done because opening a csv file of 30 years of every baseball game takes way too long to run
#we should note by separating files we are slightly compromising accuracy for speed
if (season > 2018 | season < 1993):
    print('ERROR. PLEASE ENTER YEAR BETWEEN 1993 AND 2018.\n\n')
elif (season > 2008):
    ext = '0918'
elif (season > 2000):
    ext = '0108'
else:
    ext = '9300'

retrodf = pd.read_csv(homedir + '/Desktop/stats_adjuster/retrosheet_data/retrosheet' + ext + '.csv', low_memory=False)
retrodf['game_counter'] = 1

player_ID = f.name_to_ID(player_name=player, team_city=team, year=season, df=retrodf)

#Calculate Avg
park_stats_avg = f.get_ballpark_df(stat='avg', df=retrodf)
schedule_stats_avg = f.get_schedule_stats(year=season, gamedf=retrodf, ID=player_ID, avg=True, parkdf=park_stats_avg)
playerAvg = float(input('Enter ' + player + '\'s batting average in ' + str(season) + ': '))
newSchedule_avg = f.create_new_schedule(parkdf=park_stats_avg, avg=True)
newAvg = f.convert_stats(stat=playerAvg, stat_conv=schedule_stats_avg, stat_new_sched=newSchedule_avg)
newAvg = int(round(newAvg, 3) * 1000)

#Calculate HR
park_stats_HR = f.get_ballpark_df(stat='HR', df=retrodf)
schedule_stats_HR = f.get_schedule_stats(year=season, gamedf=retrodf, ID=player_ID, avg=False, parkdf=park_stats_HR)
playerHR = int(input('Enter ' + player + '\'s homerun total in ' + str(season) + ': '))
newSchedule_HR = f.create_new_schedule(parkdf=park_stats_HR, avg=False)
newHR = f.convert_stats(stat=playerHR, stat_conv=schedule_stats_HR, stat_new_sched=newSchedule_HR)
newHR = round(newHR, 1)

#Calculate RBI
park_stats_RBI = f.get_ballpark_df(stat='RBI', df=retrodf)
schedule_stats_RBI = f.get_schedule_stats(year=season, gamedf=retrodf, ID=player_ID, avg=False, parkdf=park_stats_RBI)
playerRBI = int(input('Enter ' + player + '\'s RBI total in ' + str(season) + ': '))
newSchedule_RBI = f.create_new_schedule(parkdf=park_stats_RBI, avg=False)
newRBI = f.convert_stats(stat=playerRBI, stat_conv=schedule_stats_RBI, stat_new_sched=newSchedule_RBI)
newRBI = round(newRBI, 1)

print('\nWith a standard schedule, ' + player + ' would have hit an estimated .' + str(newAvg) + ' with ' + str(newHR) + ' homeruns ' + ' and '+ str(newRBI) + ' RBI\'s in ' + str(season) + '.\n')



     # The information used here was obtained free of
     # charge from and is copyrighted by Retrosheet.  Interested
     # parties may contact Retrosheet at 20 Sunset Rd.,
     # Newark, DE 19711.


#below used for debugging
# print('park_stats: ', park_stats_avg, '\nschedule_stats: ', schedule_stats_avg)
# print('\nnewSchedule: ', newSchedule_avg, '\nrealHR: ', playerAvg, '\nnewHR: ', newAvg)
