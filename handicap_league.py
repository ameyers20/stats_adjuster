import pandas as pd
import numpy as np

df = pd.read_csv('/Users/alex/Desktop/stats_adjuster/retrosheet_data/retrosheet0918.csv', low_memory=False)

dfr = df.copy()
dfr['rbi'] = dfr['vRBI'] + dfr['hRBI']
dfr = dfr[['home league', 'rbi']]
NLmean = np.mean(dfr.where(dfr['home league'] == 'NL')['rbi'])
ALmean = np.mean(dfr.where(dfr['home league'] == 'AL')['rbi'])

print('\nNL mean rbi: ', NLmean, '\nAL mean rbi: ', ALmean)

dfhr = df.copy()
dfhr['homers'] = dfhr['vHR'] + dfhr['hHR']
dfhr = dfhr[['home league', 'homers']]
NLmean = np.mean(dfhr.where(dfhr['home league'] == 'NL')['homers'])
ALmean = np.mean(dfhr.where(dfhr['home league'] == 'AL')['homers'])

print('\nNL mean HR: ', NLmean, '\nAL mean HR: ', ALmean)

dfa = df.copy()
dfa['average'] = (dfa['vH'] + dfa['hH']) / (dfa['vAB'] + dfa['hAB'])
dfa = dfa[['home league', 'average']]
NLmean = np.mean(dfa.where(dfa['home league'] == 'NL')['average'])
ALmean = np.mean(dfa.where(dfa['home league'] == 'AL')['average'])

print('\nNL mean batting avg: ', NLmean, '\nAL mean batting avg: ', ALmean)
#Do the same for HR avg RBI etc
