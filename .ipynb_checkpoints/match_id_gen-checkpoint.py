import requests
import json
import sys
import time
import csv
import pandas
def get_players(match_request):
    player_ids = []
    for player_id in match_request.json()["participantIdentities"]:
        print(player_id["player"]["accountId"])
        player_ids.append(player_id["player"]["accountId"])
    return player_ids

# First request made to riot that all of the other calls stem from 
URL = 'https://na1.api.riotgames.com/lol/match/v4/matches/3187138923'
params = {'api_key':sys.argv[1]}
r = requests.get(url = URL, params = params)

with open('league.csv', 'wb') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',')

features = ['gameId']
row = {"gameId": [],
      "gameCreation": [],
      "gameDuration": [],
      "queueId": [],
      "gameVersion": [],
      "gameType": [],
       "teamId": [],
       "firstBlood": [],
       "firstTower": [],
       "firstInhibitor": [],
       "firstBaron": [],
       "firstDragon": [],
       "firstRiftHerald": [],
       "towerKills": [],
       "inhibitorKills": [],
       "baronKills": [],
       "dragonKills": [],
       "vilemawKills": [],
       "riftHeraldKills": [],
       "dominionVictoryScore": [],	
       "championId_x": [],
       "pickTurn": [],
       "participantId": [],	
       "championId_y": [],
       "spell1Id": [],
       "spell2Id": [],
       "stats.win": [],
       "stats.item0": [],
       "stats.item1": [],
       "stats.item2": [],
       "stats.item3": [],
       "stats.item4": [],
       "stats.item5": [],
       "stats.item6": [],
       "stats.kills": [],
       "stats.deaths": [],
       "stats.assists": [],
       "stats.largestKillingSpree": [],	
       "stats.largestMultiKill": [],
       "stats.killingSprees": [],
       "stats.totalDamageDealt": [],
       "stats.magicDamageDealt": [],
       "stats.physicalDamageDealt": [],
       "stats.trueDamageDealt": [],
       "stats.largestCriticalStrike": [],
       "stats.totalDamageDealtToChampions": [],
       "stats.magicDamageDealtToChampions": [],
       "stats.physicalDamageDealtToChampions": [],
       "stats.trueDamageDealtToChampions": [],
       "stats.totalHeal": [],
       "stats.totalUnitsHealed": [],
       "stats.damageSelfMitigated": [],
       "stats.damageDealtToObjectives": [],
       "stats.damageDealtToTurrets": [],
       "stats.visionScore": [],
       "stats.timeCCingOthers": [],
       "stats.totalDamageTaken": [],
       "stats.magicalDamageTaken": [],
       "stats.physicalDamageTaken": [],
       "stats.trueDamageTaken": [],
       "stats.goldEarned": [],
       "stats.goldSpent": [],
       "stats.turretKills": [],
       "stats.inhibitorKills": [],
       "stats.totalMinionsKilled": [],
       "stats.neutralMinionsKilled": [],
       "stats.neutralMinionsKilledTeamJungle": [],	
       "stats.neutralMinionsKilledEnemyJungle": [],
       "stats.totalTimeCrowdControlDealt": [],
       "stats.champLevel": [],
       "stats.visionWardsBoughtInGame": [],
       "stats.sightWardsBoughtInGame": [],
       "stats.wardsPlaced": [],
       "stats.wardsKilled": [],
       "stats.firstBloodKill": [],
       "stats.firstBloodAssist": [],
       "stats.firstTowerKill": [],
       "stats.firstTowerAssist": [],
       "stats.firstInhibitorKill": [],
       "stats.firstInhibitorAssist": [],
       "stats.combatPlayerScore": [],
       "stats.objectivePlayerScore": [],
       "stats.totalPlayerScore": [],
       "stats.totalScoreRank": [],
       "stats.playerScore0": [],
       "stats.playerScore1": [],
       "stats.playerScore2": [],
       "stats.playerScore3": [],
       "stats.playerScore4": [],
       "stats.playerScore5": [],
       "stats.playerScore6": [],
       "stats.playerScore7": [],
       "stats.playerScore8": [],
       "stats.playerScore9": [],
       "stats.perk0": [],
       "stats.perk1": [],
       "stats.perk2": [],
       "stats.perk3": [],
       "stats.perk4": [],
       "stats.perk5": [],
       "stats.perkPrimaryStyle": [],
       "stats.perkSubStyle": [],
       "stats.statPerk0": [],
       "stats.statPerk1": [],
       "stats.statPerk2": [],
       "timeline.creepsPerMinDeltas.10-20": [],
       "timeline.creepsPerMinDeltas.0-10": [],
       "timeline.creepsPerMinDeltas.20-30": [],
       "timeline.xpPerMinDeltas.10-20": [],
       "timeline.xpPerMinDeltas.0-10": [],
       "timeline.xpPerMinDeltas.20-30": [],
       "timeline.goldPerMinDeltas.10-20": [],
       "timeline.goldPerMinDeltas.0-10": [],
       "timeline.goldPerMinDeltas.20-30": [],
       "timeline.damageTakenPerMinDeltas.10-20": [],
       "timeline.damageTakenPerMinDeltas.0-10": [],
       "timeline.damageTakenPerMinDeltas.20-30": [],
       "timeline.role": [],
       "timeline.lane": [],
       "player.accountId": [],
       "player.summonerName": [],
       "player.summonerId": [],
       "player.matchHistoryUri": [],
      }

print(json.dumps(r.json(), indent=4))

player_ids = get_players(r)


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
for game in games:
    gameURL = 'https://na1.api.riotgames.com/lol/match/v4/matches/' + str(game)
    new_request = requests.get(url = gameURL, params = params)
    print("This is the output for a match request")
    populate(row, new_request)
    break
#print(json.dumps(r.json()["participantIdentities"], indent = 4))


def populate(data, request):
    data['gameId'].append(new_request.json()['gameId'])