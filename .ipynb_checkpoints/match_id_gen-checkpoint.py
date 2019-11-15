import requests
import json
import sys
import time
import csv
import pandas as pd
from pandas.io.json import json_normalize
def get_players(match_request):
    player_ids = []
    for player_id in match_request.json()["participantIdentities"]:
        print(player_id["player"]["accountId"])
        player_ids.append(player_id["player"]["accountId"])
    return player_ids

# First request made to riot that all of the other calls stem from 
URL = 'https://na1.api.riotgames.com/lol/match/v4/matches/' + str(sys.argv[3])
params = {'api_key':sys.argv[1]}
r = requests.get(url = URL, params = params)

with open('league.csv', 'wb') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',')
        
# Needed columns: Allies, Counters, Runes, Spells, Win Rate, Pick Rate, Perk
# Allies = 3 champions that won the most games with this champion
# Counters=3 champions that won the most games against this champion
# Runes = Top 2 most utilized runes with this champion
# Spells= Given
# Win Rate = Wins/Total y games for champion
# Pick Rate = Picks + games / All games
# Perks = Top Perks for champion 
# Difficulty = Given
            #print(json.dumps(r.json(), indent=4))

player_ids = get_players(r)

def populate(request):
    json_request = json.loads(json.dumps(request.json()))
    game_info = json_normalize(json_request)
    game_info.drop(['teams','participants','participantIdentities'],axis=1,inplace=True)
    teams = json_normalize(json_request,record_path=['teams'],meta=['gameId'])
    teams_bans = json_normalize(json_request['teams'],record_path=['bans'],meta=['teamId'])
    r_teams_bans_f = pd.merge(teams,teams_bans,how='inner').drop('bans', axis=1)
    

    r_prtcpts = json_normalize(json_request,record_path=['participants'],meta=['gameId'])
    stats = json_normalize(r_prtcpts['stats'])
    timeline = json_normalize(r_prtcpts['timeline'])
    r_prtcpts = r_prtcpts.drop(columns=['stats', 'timeline'])
    r_prtcpts = pd.merge(timeline, r_prtcpts, on='participantId')
    r_prtcpts = pd.merge(stats, r_prtcpts,    on='participantId')
    
    r_prtcpts_id = json_normalize(json_request,record_path=['participantIdentities'],meta=['gameId'])
    player = json_normalize(r_prtcpts_id['player'])
    r_prtcpts_id = r_prtcpts_id.drop(columns=['player'])
    r_prtcpts = pd.concat([r_prtcpts, player], axis=1)
    
    match_final = pd.merge(pd.merge(pd.merge(game_info,r_teams_bans_f,on='gameId',how='inner'),r_prtcpts,
                                left_on=['gameId','teamId','pickTurn'],right_on=['gameId','teamId','participantId'],how='inner'),
                       r_prtcpts_id,on=['gameId','participantId'],how='inner')
    match_final = match_final.drop(columns=['participantId',
'longestTimeSpentLiving',
'doubleKills',
'tripleKills',
'quadraKills',
'pentaKills',
'unrealKills',
'perk0Var1',
'perk0Var2',
'perk0Var3',
'perk1Var1',
'perk1Var2',
'perk1Var3',
'perk2Var1',
'perk2Var2',
'perk2Var3',
'perk3Var1',
'perk3Var2',
'perk3Var3',
'perk4Var1',
'perk4Var2',
'perk4Var3',
'perk5Var1',
'perk5Var2',
'perk5Var3',
'participantId',
'currentPlatformId',
'currentAccountId',
'profileIcon', 'seasonId', 'mapId', 'gameMode'])
    return match_final

def get_1000_matches(player_list):
    gameIds = []
    for player in player_list:
        URL = 'https://na1.api.riotgames.com/lol/match/v4/matchlists/by-account/'+ player
        r = requests.get(url = URL, params = params)

        for match in r.json()["matches"]:
            gameIds.append(match["gameId"])
        print(len(gameIds))

        #time.sleep(1)
    return gameIds
print("All match Ids for every player in first match 3187138923")
games = get_1000_matches(player_ids)

# Note that one match ID can give us 1000 different matches
data = pd.DataFrame()
i = 0
for game in games:
    
    gameURL = 'https://na1.api.riotgames.com/lol/match/v4/matches/' + str(game)
    new_request = requests.get(url = gameURL, params = params)
    print("This is the output for a match request")
    match_data = populate(new_request)
    data = pd.concat([match_data, data], axis=0)
    if str(i) == sys.argv[2]:
        break
    i += 1

print("You collected: " + str(len("games")) + " games and " + str(data.shape[0]) + " data points!")

# This is the data, create a csv if you want 
# data