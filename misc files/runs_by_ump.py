import pandas as pd
import numpy as np
import os.path

homedir = os.path.expanduser("~") #to open the file from another computer
df = pd.read_csv(homedir + '/Desktop/stats_adjuster/retrosheet_data/retrosheet0918.csv', low_memory=False)

df['runs'] = df['visit score'] + df['home score']
ump = df[['runs', 'hpUmpID']]
ump_ind = pd.DataFrame(index = [], columns = ['runs_sum', 'num_games'])

for row in range(len(ump)):
    if (ump_ind.index.contains(ump.iloc[row]['hpUmpID'])):
        ump_ind.loc[ump.iloc[row]['hpUmpID']]['runs_sum'] += ump.iloc[row]['runs']
        ump_ind.loc[ump.iloc[row]['hpUmpID']]['num_games'] += 1
    else:
        ump_ind.loc[ump.iloc[row]['hpUmpID']] = [ump.iloc[row]['runs'], 1]

ump_ind['mean_runs'] = ump_ind['runs_sum']/ump_ind['num_games']
ump_ind = ump_ind.sort_values(by=['mean_runs'])

print(ump_ind[ump_ind['num_games'] > 30])
print('League mean: ', ump_ind['runs_sum'].sum()/ump_ind['num_games'].sum())
print('\nBill Miller: \n', ump_ind.loc['millb901'])
