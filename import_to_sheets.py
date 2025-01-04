import gspread
from oauth2client.service_account import ServiceAccountCredentials
import playerinfo
import api_key
import riot_data_functions
from datetime import datetime

apikey = api_key.api_key
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('riot_api_work\\akkers_example_code\league-api-tester-59236d391e44.json', scope)

client = gspread.authorize(creds)

sheet = client.open('akkers_data')

#Create worksheet for averages of a player
averages_player = ("AVERAGES - " + playerinfo.role + " - " + playerinfo.summoner_name + "#" + 
            playerinfo.tag_line)

averages_exists = False

for worksheet in sheet.worksheets():
    if worksheet.title == averages_player:
        sheet_instance_average = sheet.worksheet(averages_player)
        averages_exists = True
        break

if averages_exists == False:
    sheet.add_worksheet(rows=20,cols=10,title= averages_player)
    worksheet_length = len(sheet.worksheets())
    sheet_instance_average = sheet.get_worksheet(worksheet_length - 1)

#Create worksheet for past x games of a player
all_player = ("ALL GAMES - " + playerinfo.role + " - " + playerinfo.summoner_name + "#" + 
              playerinfo.tag_line)

all_exists = False

for worksheet in sheet.worksheets():
    if worksheet.title == all_player:
        sheet_instance_all = sheet.worksheet(all_player)
        all_exists = True
        break

if all_exists == False:
    sheet.add_worksheet(rows=20,cols=10,title= all_player)
    worksheet_length = len(sheet.worksheets())
    sheet_instance_all = sheet.get_worksheet(worksheet_length - 1)

df = riot_data_functions.get_player_stats (playerinfo.summoner_name, playerinfo.tag_line, playerinfo.role, playerinfo.region, playerinfo.no_games, playerinfo.queue_id, 
                              apikey)

df.to_csv("D:\Projects\leagueproject\data_csvs\\" + playerinfo.summoner_name + "_DATA", index=False)

#Following lines are seperated by whether they are a laner (i.e. top,mid,adc), a jungler, or support. 
#Certain stats are ommitted depending on relevance to role.

if (playerinfo.role == "TOP" or playerinfo.role == "MIDDLE" or playerinfo.role == "BOTTOM"):
    #AVERAGES
    lanerStats = df.groupby(['champion']).agg(
        game_count=('kills', 'count'),
        win_count=('win', 'sum'),
        mean_kills=('kills', lambda x: round(x.mean(), 2)),
        mean_deaths=('deaths', lambda x: round(x.mean(), 2)),
        mean_assists=('assists', lambda x: round(x.mean(), 2)),
        mean_kill_participation=('killParticipation', lambda x: round(x.mean(), 2)),
        mean_cs_diff_14=('csdiff14min', lambda x: round(x.mean(), 2)),
        mean_turret_plates=('turretPlatesTaken', lambda x: round(x.mean(), 2)),
        mean_gold_diff_14=('golddiff14min', lambda x: round(x.mean(), 2)),
        mean_xp_diff_14=('xpDiff14', lambda x: round(x.mean(), 2)),
        mean_dmg_14=('dmgChamps14', lambda x: round(x.mean(), 2)),
        mean_total_dmg=('totalDmgChamps', lambda x: round(x.mean(), 2)),
        mean_dmg_percentage=('teamDamagePercentage', lambda x: round(x.mean(), 2)),
        mean_vision_wards=('visionWardsBoughtInGame', lambda x: round(x.mean(), 2)),
    ).reset_index()

    lanerStats = lanerStats.sort_values(by='game_count',ascending=False).reset_index(drop=True)

    sheet_instance_average.clear()
    sheet_instance_average.insert_row(["DATE: ", datetime.today().strftime('DATE, %Y-%m-%d TIME, %H-%M-%S')])
    sheet_instance_average.insert_row([])
    sheet_instance_average.insert_rows(lanerStats.values.tolist())
    sheet_instance_average.insert_row(['Champion','No.Games','No.wins','Kills','Deaths','Assists', 'KP%', 'CSD@14','Plates Taken','GD@14',
                            'XPD@14', 'DMGtC@14', 'Total DMGtC', 'DMG %', 'Pinks Bought'])

    df = df.reset_index(drop=True)

    df = df.drop("jungleCsdiff14", axis='columns')
    df = df.drop("visionScore", axis='columns')
    df = df.drop("visionScorePerMinute", axis='columns')
    df = df.drop("controlWardsPlaced", axis='columns')
    df = df.drop("wardTakedowns", axis='columns')
    df = df.drop("wardsPlaced", axis='columns')
    df = df.drop("completeSupportQuestInTime", axis='columns')

    df = df.round(2)

    sheet_instance_all.clear()
    sheet_instance_all.insert_row(["DATE: ", datetime.today().strftime('DATE, %Y-%m-%d TIME, %H-%M-%S')])
    sheet_instance_all.insert_row([])

    sheet_instance_all.insert_rows(df.values.tolist())

    sheet_instance_all.insert_row(['Champion', 'Champion Vs.', 'Kills', 'Deaths', 'Assists', 'Win', 'KP%', 'CSD@14', 'Plates Taken', 'GD@14', 
                                      'XPD@14', 'DMGtC@14', 'Total DMGtC', 'DMG %', 'Pinks Bought'])

    
if (playerinfo.role == "JUNGLE"):
    lanerStats = df.groupby(['champion']).agg(
        game_count=('kills', 'count'),
        win_count=('win', 'sum'),
        mean_kills=('kills', lambda x: round(x.mean(), 2)),
        mean_deaths=('deaths', lambda x: round(x.mean(), 2)),
        mean_assists=('assists', lambda x: round(x.mean(), 2)),
        mean_kill_participation=('killParticipation', lambda x: round(x.mean(), 2)),
        mean_cs_diff_14=('csdiff14min', lambda x: round(x.mean(), 2)),
        mean_jungle_cs_diff_14=('jungleCsdiff14', lambda x: round(x.mean(), 2)),
        mean_turret_plates=('turretPlatesTaken', lambda x: round(x.mean(), 2)),
        mean_gold_diff_14=('golddiff14min', lambda x: round(x.mean(), 2)),
        mean_xp_diff_14=('xpDiff14', lambda x: round(x.mean(), 2)),
        mean_dmg_14=('dmgChamps14', lambda x: round(x.mean(), 2)),
        mean_total_dmg=('totalDmgChamps', lambda x: round(x.mean(), 2)),
        mean_dmg_percentage=('teamDamagePercentage', lambda x: round(x.mean(), 2)),
        mean_vision_wards=('visionWardsBoughtInGame', lambda x: round(x.mean(), 2)),
        mean_vision_score=('visionScore', lambda x: round(x.mean(), 2))
    ).reset_index()

    lanerStats = lanerStats.sort_values(by='game_count',ascending=False).reset_index(drop=True)

    sheet_instance_average.insert_rows(lanerStats.values.tolist())
    sheet_instance_average.insert_row(['Champion','No.Games','No.wins','Kills','Deaths','Assists','KP%','CSD@14',
                               'JG CSD@14','Plates Taken','GD@14','XPD@14', 'DMGtC@14', 'Total DMGtC',
                                'DMG %', 'Pinks bought', 'Vision score'])

    df = df.reset_index(drop=True)

    df = df.drop("visionScorePerMinute", axis='columns')
    df = df.drop("controlWardsPlaced", axis='columns')
    df = df.drop("wardTakedowns", axis='columns')
    df = df.drop("wardsPlaced", axis='columns')
    df = df.drop("completeSupportQuestInTime", axis='columns')

    df = df.round(2)

    sheet_instance_all.insert_rows(df.values.tolist())

    sheet_instance_all.insert_row(['Champion', 'Champion Vs.', 'Kills', 'Deaths', 'Assists', 'Win', 'KP%', 'CSD@14',
                                    'JG CSD@14', 'Plates Taken', 'GD@14', 'XPD@14', 'DMGtC@14', 'Total DMGtC', 
                                    'DMG %', 'Vision Score', 'Pinks Bought'])

if (playerinfo.role == "UTILITY"):
    lanerStats = df.groupby(['champion']).agg(
        game_count=('kills', 'count'),
        win_count=('win', 'sum'),
        mean_kills=('kills', lambda x: round(x.mean(), 2)),
        mean_deaths=('deaths', lambda x: round(x.mean(), 2)),
        mean_assists=('assists', lambda x: round(x.mean(), 2)),
        mean_kill_participation=('killParticipation', lambda x: round(x.mean(), 2)),
        mean_turret_plates=('turretPlatesTaken', lambda x: round(x.mean(), 2)),
        mean_gold_diff_14=('golddiff14min', lambda x: round(x.mean(), 2)),
        mean_xp_diff_14=('xpDiff14', lambda x: round(x.mean(), 2)),
        mean_dmg_14=('dmgChamps14', lambda x: round(x.mean(), 2)),
        mean_total_dmg=('totalDmgChamps', lambda x: round(x.mean(), 2)),
        mean_dmg_percentage=('teamDamagePercentage', lambda x: round(x.mean(), 2)),
        mean_vision_score=('visionScore', lambda x: round(x.mean(), 2)),
        mean_vspm=('visionScorePerMinute', lambda x: round(x.mean(), 2)),
        mean_vision_wards=('visionWardsBoughtInGame', lambda x: round(x.mean(), 2)),
        mean_control_wards_placed=('controlWardsPlaced', lambda x: round(x.mean(), 2)),
        mean_wards_takedowns=('wardTakedowns', lambda x: round(x.mean(), 2)),
        mean_wards_placed=('wardsPlaced', lambda x: round(x.mean(), 2)),
        mean_support_quest_time=('completeSupportQuestInTime', lambda x: round(x.mean(), 2))
    ).reset_index()

    lanerStats = lanerStats.sort_values(by='game_count',ascending=False).reset_index(drop=True)

    sheet_instance_average.insert_rows(lanerStats.values.tolist())
    sheet_instance_average.insert_row(['Champion','No.Games','No.wins','Kills','Deaths','Assists','KP%', 'Plates Taken','GD@14',
                                      'XPD@14', 'DMGtC@14', 'Total DMGtC', 'DMG %', 'Vision Score', 'Vision Score p/m', 'Pinks Bought',
                                      'Pinks Placed', 'Ward Takedowns', 'Wards Placed', 'Supp Quest Time'])
    
    df = df.reset_index(drop=True)

    df = df.drop("csdiff14min", axis='columns')
    df = df.drop("jungleCsdiff14", axis='columns')

    df = df.round(2)

    sheet_instance_all.insert_rows(df.values.tolist())

    sheet_instance_all.insert_row(['Champion', 'Champion Vs.', 'Kills', 'Deaths', 'Assists', 'Win', 'KP%', 'Plates Taken', 'GD@14', 
                                      'XPD@14', 'DMGtC@14', 'Total DMGtC', 'DMG %', 'Vision Score', 'Vision Score p/m', 'Pinks bought',
                                      'Pinks placed', 'Ward Takedowns', 'Wards Placed', 'Supp Quest Time'])
    
sheet_instance_average.format("A1:Y1", {
    "backgroundColor": {
      "red": 0.0,
      "green": 0.0,
      "blue": 0.0
    },
    "horizontalAlignment": "CENTER",
    "textFormat": {
      "foregroundColor": {
        "red": 1.0,
        "green": 1.0,
        "blue": 1.0
      },
      "fontSize": 12,
      "bold": True
    }
})

sheet_instance_all.format("A1:Y1", {
    "backgroundColor": {
      "red": 0.0,
      "green": 0.0,
      "blue": 0.0
    },
    "horizontalAlignment": "CENTER",
    "textFormat": {
      "foregroundColor": {
        "red": 1.0,
        "green": 1.0,
        "blue": 1.0
      },
      "fontSize": 12,
      "bold": True
    }
})

