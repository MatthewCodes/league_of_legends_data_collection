import requests
import json
import sys
import time
import csv

URL = 'https://na1.api.riotgames.com/lol/match/v4/matches/3187138923'

params = {'api_key':sys.argv[1]}

r = requests.get(url = URL, params = params)
player_ids = []
with open('league.csv', 'wb') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',')

features = []
row = dict()
#print(json.dumps(r.json(), indent=4))
for player_id in r.json()["participantIdentities"]:
    print(player_id["player"]["accountId"])
    player_ids.append(player_id["player"]["accountId"])

gameIds = []
for player in player_ids:
    URL = 'https://na1.api.riotgames.com/lol/match/v4/matchlists/by-account/'+ player
    print(URL)
    r = requests.get(url = URL, params = params)
    #print(json.dumps(r.json()))
    #matches = [x for x in r.json()["matches"]]
    for match in r.json()["matches"]:
        gameIds.append(match["gameId"])
    print(len(gameIds))
    
    time.sleep(1)
    
print("All match Ids for every player in first match 3187138923")
print(gameIds)

# Note that one match ID can give us 1000 different matches
for game in gameIds:
    gameURL = 'https://na1.api.riotgames.com/lol/match/v4/matches/' + str(game)
    new_request = requests.get(url = gameURL, params = params)
    print("This is the output for a match request")
    print(json.dumps(new_request.json(), indent = 4))
    break
#print(json.dumps(r.json()["participantIdentities"], indent = 4))


