import pandas as pd
import numpy as np
import math as m

#given a player name, season and team, finds the ID associated with that player
#without it, players with the same name would both be counted, which obviously leads to drastic problems
def name_to_ID(player_name, team_city, year, df):
    df1 = df.copy()
    df1 = df1[(df1['home team'] == team_city) & (df1['Date'] < (year * 10001))]
    for i in range(len(df1)):
        if (df.iloc[i]['hBat1Name'] == player_name):
            return df.iloc[i]['hBat1ID']
        if (df.iloc[i]['hBat2Name'] == player_name):
            return df.iloc[i]['hBat2ID']
        if (df.iloc[i]['hBat3Name'] == player_name):
            return df.iloc[i]['hBat3ID']
        if (df.iloc[i]['hBat4Name'] == player_name):
            return df.iloc[i]['hBat4ID']
        if (df.iloc[i]['hBat5Name'] == player_name):
            return df.iloc[i]['hBat5ID']
        if (df.iloc[i]['hBat6Name'] == player_name):
            return df.iloc[i]['hBat6ID']
        if (df.iloc[i]['hBat7Name'] == player_name):
            return df.iloc[i]['hBat7ID']
        if (df.iloc[i]['hBat8Name'] == player_name):
            return df.iloc[i]['hBat8ID']
        if (df.iloc[i]['hBat9Name'] == player_name):
            return df.iloc[i]['hBat9ID']
    print('ERROR PLAYER NOT FOUND')
    return None;

#Given a stat like HR,avg,RBI and an original retrosheet dataframe, will
#return a dataframe for the mean and std of the stat for a single mean hitter
def get_ballpark_df(stat, df):
    df1 = df.copy()
    if (stat == 'HR'):
        df1['stat'] = (df1['hHR'] + df1['vHR'])
        league_conv = 1.1215 #AL/NL to account for the DH, these were computed on handicap_league.py
    elif (stat == 'RBI'):
        df1['stat'] = (df1['hRBI'] + df1['vRBI'])
        league_conv = 1.0504
    elif (stat == 'avg'):
        df1['stat'] = (df1['hH'] + df1['vH']) / (df['hAB'] + df['vAB'])
        league_conv = 1.0138

    df1 = df1[['Ballpark ID', 'stat', 'home league', 'game_counter']]
    parkdf = pd.DataFrame(columns = ['parkID', 'mean_stat', 'var_stat', 'num_games']) #add std

    i = 0
    for park in df1['Ballpark ID'].unique():
        mean = np.mean(df1.where(df1['Ballpark ID'] == park)['stat'])
        if (stat != 'avg'):
            mean /= 18
        if(df1[df1['Ballpark ID'] == park].iloc[0]['home league'] == 'NL'):
            mean *= league_conv #to account for the DH
        var = np.var(df1.where(df1['Ballpark ID'] == park)['stat'])
        if (stat != 'avg'):
            var /= 18
        num_games = np.sum(df1.where(df1['Ballpark ID'] == park)['game_counter'])
        parkdf.loc[i] = [park, mean, var, num_games]
        i+=1

    parkdf = parkdf.sort_values(by=['mean_stat']).set_index('parkID')

    return parkdf

#finds ballparks player played in and creates a mean and variance for that schedule
def get_schedule_stats(year, gamedf, ID, avg, parkdf): #name, ballparkdf
    df1 = gamedf.copy()
    df1 = df1[(df1['Date'] > (year * 10000)) & (df1['Date'] < (year * 10001))] #narrow down to specific season, works cause year is an int
    df1 = df1[(df1['vBat1ID'] == ID) | (df1['vBat2ID'] == ID) | (df1['vBat3ID'] == ID) | (df1['vBat4ID'] == ID) | (df1['vBat5ID'] == ID) | (df1['vBat6ID'] == ID) | (df1['vBat7ID'] == ID) | (df1['vBat8ID'] == ID) | (df1['vBat9ID'] == ID) | (df1['hBat1ID'] == ID) | (df1['hBat2ID'] == ID) | (df1['hBat3ID'] == ID) | (df1['hBat4ID'] == ID) | (df1['hBat5ID'] == ID) | (df1['hBat6ID'] == ID) | (df1['hBat7ID'] == ID) | (df1['hBat8ID'] == ID) | (df1['hBat9ID'] == ID)]
    #line above narrows down to games started by the player
    df1 = df1[['Ballpark ID', 'game_counter']].reset_index()

    schedule_mean = 0
    schedule_var = 0

    for i in range(len(df1)): #loop adds up the mean and var for individual games to get season total
        schedule_mean += parkdf.loc[df1.iloc[i]['Ballpark ID']]['mean_stat']
        schedule_var += parkdf.loc[df1.iloc[i]['Ballpark ID']]['var_stat']

    #if batting average we want the mean of average not the sum
    if(avg):
        schedule_mean /= len(df1)
        schedule_var /= len(df1)

    schedule_std = m.sqrt(schedule_var) #converts variance to std

    #below converts the schedule stats to full season, since players don't start all 162: see assumptions
    #note that for average we don't want this, thus it returns beforehand
    games_started = np.sum(df1['game_counter'])
    full_season = 162/games_started
    #note that for average we don't want this, thus it returns beforehand
    if(avg):
        return (schedule_mean, schedule_std, full_season)

    schedule_mean *= full_season
    schedule_std *= full_season

    return (schedule_mean, schedule_std, full_season)

#builds a standardized schedule weighted by
def create_new_schedule(parkdf, avg): 
    parkdf1 = parkdf.copy()
    tot_games = np.sum(parkdf1['num_games'])
    parkdf1['mean_times_games'] = parkdf1['mean_stat'] * parkdf1['num_games']
    parkdf1['var_times_games'] = parkdf1['var_stat'] * parkdf1['num_games']
    new_mean = (np.sum(parkdf1['mean_times_games']) / tot_games)
    new_var = (np.sum(parkdf1['var_times_games']) / tot_games)
    if (not avg):
        new_mean *= 162
        new_var *= 162
    new_std = m.sqrt(new_var)

    return (new_mean, new_std)

#takes in stats and returns converted stat to new schedule
def convert_stats(stat, stat_conv, stat_new_sched):
    dfm_stat = (stat - stat_conv[0])/stat_conv[1] #dvm: stdeviations from mean
    new_stat = (dfm_stat)*(stat_new_sched[1]) + stat_new_sched[0]

    return new_stat
