import requests
import pandas as pd
import time

def get_puuid(summoner_name, tag_line, region, api_key):
    api_url = ("https://" + 
               region + 
               ".api.riotgames.com/riot/account/v1/accounts/by-riot-id/" + 
               summoner_name + 
               "/" + 
               tag_line + 
                "?api_key=" + api_key)

    response = requests.get(api_url)
    account_data = response.json()
    puuid = account_data['puuid']
    return puuid


def get_match_ids(puuid, region, no_games, queue_id, api_key):
    api_url = ("https://" + 
               region +
                ".api.riotgames.com/lol/match/v5/matches/by-puuid/" + 
                puuid +
                "/ids?start=0" +
                "&count=" +
                str(no_games) +
                "&queue=" +
                str(queue_id) + 
                "&api_key=" +
                api_key            
            )

    response = requests.get(api_url)
    match_ids = response.json()
    return match_ids

def get_match_data(match_id, region, api_key):
    api_url = ("https://" +
               region +
               ".api.riotgames.com/lol/match/v5/matches/" +
               match_id +
               "?api_key=" +
               api_key)
    while True:
        response = requests.get(api_url)
        if response.status_code == 429:
            print("Rate Limit hit for getting match data, sleeping for 10 seconds")
            time.sleep(10)
            continue
        match_data = response.json()
        return match_data
    
def get_player_data(match_data, puuid):
    participants = match_data['metadata']['participants']
    player_index = participants.index(puuid)
    return match_data['info']['participants'][player_index]
    
def get_match_timeline(match_id, region, api_key):
    api_url = ("https://" + 
               region + 
               ".api.riotgames.com/lol/match/v5/matches/" + 
               match_id + 
               "/timeline" + 
               "?api_key=" +
               api_key)
    
    while True:
        response = requests.get(api_url)
        if response.status_code == 429:
            print("Rate Limit hit for getting match timeline, sleeping for 10 seconds")
            time.sleep(10)
            continue
        match_data = response.json()
        return match_data

def get_player_stats_at_time(match_timeline, puuid, frame_no):
    participant_info = match_timeline['info']['participants']
    participant_id = 0
    for participant in participant_info:
        if (participant['puuid'] == puuid):
            participant_id = participant['participantId']
    stats_at_time = match_timeline['info']['frames'][frame_no]['participantFrames'][str(participant_id)]
    return stats_at_time

def find_lane_opponent_puuid(match_data, player_data):
    role = player_data['individualPosition']
    participants = match_data['info']['participants']
    opponent_puuid = ""
    for participant in participants:
        if participant['individualPosition'] == role and (participant['puuid'] != player_data['puuid']):
            opponent_puuid = participant['puuid']
    return opponent_puuid

def gather_all_data(puuid, role, match_ids, region, api_key):
    data = {
        'champion': [],
        'opponentChampion': [],
        'kills': [],
        'deaths': [],
        'assists': [],
        'win': [],
        'killParticipation': [],
        'csdiff14min': [],
        'jungleCsdiff14': [],
        'turretPlatesTaken': [],
        'golddiff14min': [],
        'xpDiff14': [],
        'dmgChamps14': [],
        'totalDmgChamps': [],
        'teamDamagePercentage': [],
        'visionScore': [],
        'visionScorePerMinute': [],
        'visionWardsBoughtInGame': [],
        'controlWardsPlaced': [],
        'wardTakedowns': [],
        'wardsPlaced': [],
        'completeSupportQuestInTime': []
    }
    
    for match_id in match_ids:

        match_data = get_match_data(match_id, region, api_key)
        player_data = get_player_data(match_data, puuid)

        if role.upper() == player_data['individualPosition']:
            match_timeline = get_match_timeline(match_id, region, api_key)

            #if match is less than 14 mins, dont take data
            if ((match_data['info']['gameDuration'] / 60) < 14):
                continue

            #specific opponent matchup data
            opponent_puuid = find_lane_opponent_puuid(match_data,player_data)
            opponent_player_data = get_player_data(match_data,opponent_puuid)
            stats_at_14 = get_player_stats_at_time(match_timeline,puuid,14)
            opponent_stats_at_14 = get_player_stats_at_time(match_timeline,opponent_puuid,14)

            champion = player_data['championName']
            opponent_champ = opponent_player_data['championName']
            k = player_data['kills']
            d = player_data['deaths']
            a = player_data['assists']
            win = player_data['win']

            #laner cs diff example
            csdiff14min = stats_at_14['minionsKilled'] - opponent_stats_at_14['minionsKilled']

            tpt = player_data['challenges']['turretPlatesTaken']
            golddiff14min = stats_at_14['totalGold'] - opponent_stats_at_14['totalGold']
            xpDiff14 = stats_at_14['xp'] - opponent_stats_at_14['xp']
            dmgChamps14 = stats_at_14['damageStats']['totalDamageDoneToChampions']
            totalDmgChamps = player_data['totalDamageDealtToChampions']

            #jungle cs diff example
            jungleCsdiff14 = stats_at_14['jungleMinionsKilled'] - opponent_stats_at_14['jungleMinionsKilled']
            
            visionScore = player_data['visionScore']
            visWardsBought = player_data['visionWardsBoughtInGame']
            wardsPlaced = player_data['wardsPlaced']
            controlWardsPlaced = player_data['challenges']['controlWardsPlaced']
            timeToCompleteSuppQuest = player_data['challenges']['completeSupportQuestInTime']
            killParticipation = player_data['challenges']['killParticipation'] * 100
            visionScorePerMinute = player_data['challenges']['visionScorePerMinute']
            wardTakedowns = player_data['challenges']['wardTakedowns']
            teamDamagePercentage = player_data['challenges']['teamDamagePercentage'] * 100

            data['champion'].append(champion)
            data['opponentChampion'].append(opponent_champ)
            data['kills'].append(k)
            data['deaths'].append(d)
            data['assists'].append(a)
            data['win'].append(win)    
            data['csdiff14min'].append(csdiff14min)
            data['turretPlatesTaken'].append(tpt)
            data['golddiff14min'].append(golddiff14min)
            data['xpDiff14'].append(xpDiff14)
            data['dmgChamps14'].append(dmgChamps14)
            data['totalDmgChamps'].append(totalDmgChamps)
            data['jungleCsdiff14'].append(jungleCsdiff14)
            data['visionScore'].append(visionScore)
            data['visionWardsBoughtInGame'].append(visWardsBought)
            data['wardsPlaced'].append(wardsPlaced)
            data['controlWardsPlaced'].append(controlWardsPlaced)
            data['completeSupportQuestInTime'].append(timeToCompleteSuppQuest)
            data['killParticipation'].append(killParticipation)
            data['visionScorePerMinute'].append(visionScorePerMinute)
            data['wardTakedowns'].append(wardTakedowns)
            data['teamDamagePercentage'].append(teamDamagePercentage)
        
    df = pd.DataFrame(data)
    df['win'] = df['win'].astype(int)

    return df

def get_player_stats(summoner_name, tag_line, role, region, no_games, queue_id, api_key):
    puuid = get_puuid(summoner_name, tag_line, region, api_key)
    match_ids = get_match_ids(puuid, region, no_games, queue_id, api_key)
    df = gather_all_data(puuid, role, match_ids,region,api_key)
    return df