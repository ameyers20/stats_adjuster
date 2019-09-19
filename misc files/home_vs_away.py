import pandas as pd
import numpy as np
import os.path

homedir = os.path.expanduser("~") #to open the file from another computer
dfr = pd.read_csv(homedir + '/Desktop/stats_adjuster/retrosheet_data/retrosheet0918.csv', low_memory=False)

dfr = dfr[['Ballpark ID', 'hH', 'hAB', 'vH', 'vAB','hHR', 'vHR','hRBI', 'vRBI', 'home team']]
dfr['game_counter'] = 1 #allows us to sum up games played at a park, drop small sample sizes
parkdf = pd.DataFrame(columns = ['parkID', 'team', 'AVG_Dif', 'HR_Dif','RBI_Dif', 'seasons'])

i = 0
for park in dfr['Ballpark ID'].unique():
    #computes average dif in percentage points (1/1000)
    hHsum = np.sum(dfr.where(dfr['Ballpark ID'] == park)['hH'])
    hABsum = np.sum(dfr.where(dfr['Ballpark ID'] == park)['hAB'])
    vHsum = np.sum(dfr.where(dfr['Ballpark ID'] == park)['vH'])
    vABsum = np.sum(dfr.where(dfr['Ballpark ID'] == park)['vAB'])
    avg_dif = int(round(hHsum/hABsum - vHsum/vABsum, 3) * 1000)

    hHRmean = np.mean(dfr.where(dfr['Ballpark ID'] == park)['hHR'])
    vHRmean = np.mean(dfr.where(dfr['Ballpark ID'] == park)['vHR'])
    HR_dif = round(hHRmean - vHRmean, 3)

    hRBImean = np.mean(dfr.where(dfr['Ballpark ID'] == park)['hRBI'])
    vRBImean = np.mean(dfr.where(dfr['Ballpark ID'] == park)['vRBI'])
    rbi_dif = round(hRBImean - vRBImean, 3)

    num_season = np.sum(dfr.where(dfr['Ballpark ID'] == park)['game_counter']) / 81
    team = dfr[dfr['Ballpark ID'] == park].iloc[0]['home team']
    parkdf.loc[i] = [park, team, avg_dif, HR_dif, rbi_dif, num_season]
    i+=1

parkdf = parkdf[parkdf['seasons'] >= 1]
print(parkdf)

# dfr['rbi'] = dfr['vRBI'] + dfr['hRBI']
# dfr = dfr[['home league', 'rbi']]
# NLmean = np.mean(dfr.where(dfr['home league'] == 'NL')['rbi'])
# ALmean = np.mean(dfr.where(dfr['home league'] == 'AL')['rbi'])
