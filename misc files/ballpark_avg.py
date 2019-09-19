import pandas as pd
import numpy as np
import os.path

homedir = os.path.expanduser("~") #to open the file from another computer
df = pd.read_csv(homedir + '/Desktop/stats_adjuster/retrosheet_data/retrosheet0918.csv', low_memory=False)
df['runs'] = df['visit score'] + df['home score']
df = df[['Ballpark ID', 'runs', 'home team']]
df['game_counter'] = 1 #allows us to sum up games played at a park, drop small sample sizes
parkdf = pd.DataFrame(columns = ['parkID', 'team', 'mean_runs', 'num_games'])

i = 0
for park in df['Ballpark ID'].unique():
    avg = np.mean(df.where(df['Ballpark ID'] == park)['runs'])
    num_games = np.sum(df.where(df['Ballpark ID'] == park)['game_counter'])
    team = df[df['Ballpark ID'] == park].iloc[0]['home team']
    parkdf.loc[i] = [park, team, avg, num_games]
    i+=1

#mostly touching up data below for presentation
parkdf = parkdf[parkdf['num_games'] > 100]
parkdf = parkdf.sort_values(by=['mean_runs']).set_index('parkID').drop('num_games', axis = 1)

print(parkdf, '\n', len(parkdf), ' total ballparks\n', 'MLB average: ', np.mean(parkdf['mean_runs']))
