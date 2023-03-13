#/bin/python3
import json
import os
import shutil
from datetime import datetime
import requests
import pandas as pd

TOP = 0
JUNGLE = 1
MID = 2
ADC = 3
SUPP = 4
COACH = 5

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

project_path = '~/Documents/FantasyStatsScripts'
base_path = os.path.expanduser(project_path)
data_path = os.path.join(base_path, 'FantasyStats')

def initData(cookie):
    ligues = ['lec', 'lfl', 'superliga']

    for ligue in ligues:
        getItems(ligue, cookie)
        getPlayers(ligue, cookie)
        getMatchs(ligue, cookie)
        getGamesResult(ligue, cookie)


def initDataLeague(cookie, ligue):
    getItems(ligue, cookie)
    getPlayers(ligue, cookie)
    getMatchs(ligue, cookie)
    getGamesResult(ligue, cookie)


def getItems(ligue, cookie):
    if ligue == 'superliga':
        r = requests.get('https://api-' + ligue + '.superfantasylol.com/api/v1/itemcards', headers={
            'cookie': cookie.replace(u"\u2018", "'").replace(u"\u2019", "'"),
            'origin': 'https://' + 'lvp' + '.superfantasylol.com',
            'referer': 'https://' + 'lvp' + '.superfantasylol.com/',
            'content-language': 'fr'
        })
    else :
        r = requests.get('https://api-' + ligue + '.superfantasylol.com/api/v1/itemcards', headers={
            'cookie': cookie.replace(u"\u2018", "'").replace(u"\u2019", "'"),
            'origin': 'https://' + ligue + '.superfantasylol.com',
            'referer': 'https://' + ligue + '.superfantasylol.com',
            'content-language': 'fr'

        })
    result = json.loads(r.text)

    # ecriture des logs
    os.chdir(base_path)
    with open(ligue + '-items2.json', 'w+') as outfile:
        json.dump(result.get('data'), outfile, default=str)

    print('Items ' + ligue + ' importés')


def getPlayers(ligue, cookie):
    if ligue == 'superliga':
        r = requests.get('https://api-' + ligue + '.superfantasylol.com/api/v1/playerinfos', headers={
            'cookie': cookie.replace(u"\u2018", "'").replace(u"\u2019", "'"),
            'origin': 'https://' + 'lvp' + '.superfantasylol.com',
            'referer': 'https://' + 'lvp' + '.superfantasylol.com/',
            'content-language': 'fr'
        })
    else :
        r = requests.get('https://api-' + ligue + '.superfantasylol.com/api/v1/playerinfos', headers={
            'cookie': cookie.replace(u"\u2018", "'").replace(u"\u2019", "'"),
            'origin': 'https://' + ligue + '.superfantasylol.com',
            'referer': 'https://' + ligue + '.superfantasylol.com',
            'content-language': 'fr'
        })
    result = json.loads(r.text)

    # ecriture des logs
    os.chdir(base_path)
    with open(ligue + '-players.json', 'w+') as outfile:
        json.dump(result.get('data'), outfile, default=str)

    print('Players ' + ligue + ' importés')


def getMatchs(ligue, cookie):
    if ligue == 'superliga':
        r = requests.get('https://api-' + ligue + '.superfantasylol.com/api/v1/gamedays', headers={
            'cookie': cookie.replace(u"\u2018", "'").replace(u"\u2019", "'"),
            'origin': 'https://' + 'lvp' + '.superfantasylol.com',
            'referer': 'https://' + 'lvp' + '.superfantasylol.com/',
            'content-language': 'fr'
        })
    else :
        r = requests.get('https://api-' + ligue + '.superfantasylol.com/api/v1/gamedays', headers={
            'cookie': cookie.replace(u"\u2018", "'").replace(u"\u2019", "'"),
            'origin': 'https://' + ligue + '.superfantasylol.com',
            'referer': 'https://' + ligue + '.superfantasylol.com/',
            'content-language': 'fr'
        })
    result = json.loads(r.text).get('data')
    gamesId = []
    for game in result:
        for match in game.get('matches'):
            if len(match.get('games')) > 0:
                for game in match.get('games'):
                    gamesId.append(game.get('id'))
    gamesId.reverse()

    # #ecriture des logs
    os.chdir(base_path)
    with open(ligue + '-matchs.json', 'w+') as outfile:
        json.dump(gamesId, outfile, default=str)

    print('Matchs ' + ligue + ' importés')


def getGamesResult(ligue, cookie):
    os.chdir(base_path)
    with open(ligue + '-matchs.json') as data:
        top = []
        jungle = []
        mid = []
        adc = []
        supp = []
        coach = []
        matchesId = json.load(data)
        for id in matchesId:
            if ligue == 'superliga':
                r = requests.get('https://api-' + ligue + '.superfantasylol.com/api/v1/games/' + id, headers={
                    'cookie': cookie.replace(u"\u2018", "'").replace(u"\u2019", "'"),
                    'origin': 'https://' + 'lvp' + '.superfantasylol.com',
                    'referer': 'https://' + 'lvp' + '.superfantasylol.com/',
                    'content-language': 'fr'
                })
            else:
                r = requests.get('https://api-' + ligue + '.superfantasylol.com/api/v1/games/' + id, headers={
                    'cookie': cookie.replace(u"\u2018", "'").replace(u"\u2019", "'"),
                    'origin': 'https://' + ligue + '.superfantasylol.com',
                    'referer': 'https://' + ligue + '.superfantasylol.com/',
                    'content-language': 'fr'
                })

            result = json.loads(r.text).get('data')
            if result is not None:
                local = result.get('local').get('team').get('shortName')
                visitor = result.get('visitor').get('team').get('shortName')
                print_message = local + ' - ' + visitor
                top.append({
                    'playerId': result.get('local').get('players')[TOP].get('player').get('nickname'),
                    'items': result.get('local').get('players')[TOP].get('items')
                })
                top.append({
                    'playerId': result.get('visitor').get('players')[TOP].get('player').get('nickname'),
                    'items': result.get('visitor').get('players')[TOP].get('items')
                })

                jungle.append({
                    'playerId': result.get('local').get('players')[JUNGLE].get('player').get('nickname'),
                    'items': result.get('local').get('players')[JUNGLE].get('items')
                })
                jungle.append({
                    'playerId': result.get('visitor').get('players')[JUNGLE].get('player').get('nickname'),
                    'items': result.get('visitor').get('players')[JUNGLE].get('items')
                })

                mid.append({
                    'playerId': result.get('local').get('players')[MID].get('player').get('nickname'),
                    'items': result.get('local').get('players')[MID].get('items')
                })
                mid.append({
                    'playerId': result.get('visitor').get('players')[MID].get('player').get('nickname'),
                    'items': result.get('visitor').get('players')[MID].get('items')
                })

                adc.append({
                    'playerId': result.get('local').get('players')[ADC].get('player').get('nickname'),
                    'items': result.get('local').get('players')[ADC].get('items')
                })
                adc.append({
                    'playerId': result.get('visitor').get('players')[ADC].get('player').get('nickname'),
                    'items': result.get('visitor').get('players')[ADC].get('items')
                })

                supp.append({
                    'playerId': result.get('local').get('players')[SUPP].get('player').get('nickname'),
                    'items': result.get('local').get('players')[SUPP].get('items')
                })
                supp.append({
                    'playerId': result.get('visitor').get('players')[SUPP].get('player').get('nickname'),
                    'items': result.get('visitor').get('players')[SUPP].get('items')
                })

                coach.append({
                    'playerId': result.get('local').get('players')[COACH].get('player').get('nickname'),
                    'items': result.get('local').get('players')[COACH].get('items')
                })
                coach.append({
                    'playerId': result.get('visitor').get('players')[COACH].get('player').get('nickname'),
                    'items': result.get('visitor').get('players')[COACH].get('items')
                })

                print('Import game ' + print_message + ' terminé')
    result = {
        'top': top,
        'jungler': jungle,
        'mid': mid,
        'adc': adc,
        'support': supp,
        'coach': coach,
    }
    with open(ligue + '-itemsResults2.json', 'w+') as results:
        json.dump(result, results, default=str)

    print('Games results ' + ligue + ' importés')


def getStats(role, ligue, action):
    os.chdir(base_path)
    with open('./' + ligue + '-itemsResults2.json') as results:
        roleResult = []
        for result in json.load(results).get(role):
            roleResult.append(result.get('items'))
        # print(roleResult)
    with open('./' + ligue + '-items2.json') as items:
        object = {}
        itemsData = json.load(items)
        for item in itemsData:
            itemId = item.get('id')
            name = ''
            for translation in item.get('translations'):
                if translation.get('locale') == 'fr':
                    name = translation.get('name')
                elif translation.get('locale') == 'en':
                    en_name = translation.get('name')
            isValid = sum(x.get(itemId) is not None and x.get(itemId) > 0 for x in roleResult)
            if isValid > 0:
                object[name] = {}
                object[name]['Nom Anglais'] = en_name
                object[name]["nb games valide"] = isValid
                object[name]["total games"] = len(roleResult)
                object[name]["ratio"] = round(sum(x.get(itemId) is not None and x.get(itemId) > 0 for x in roleResult) / len(
                    roleResult), 2)
                object[name]["%"] = "{:.0%}".format(
                    sum(x.get(itemId) is not None and x.get(itemId) > 0 for x in roleResult) / len(roleResult))
                total = 0
                for x in roleResult:
                    if x.get(itemId) is not None and x.get(itemId) > 0:
                        total += x.get(itemId)
                if sum(x.get(itemId) is not None and x.get(itemId) > 0 for x in roleResult) > 0:
                    object[name]["pts moy"] = round(total / sum(
                        x.get(itemId) is not None and x.get(itemId) > 0 for x in roleResult), 2)
                else:
                    object[name]["pts moy"] = 0

                object[name]["pts moy total"] = round(total / len(roleResult), 2)
                object[name]["total point"] = total
                object[name]["cout"] = item.get('baseCost')
                if object[name]["cout"] > 0:
                    object[name]["pts par cout moy"] = round(object[name]["pts moy"] / object[name]["cout"], 2)
                else:
                    object[name]["pts par cout moy"] = 'Gratuit'

                if object[name]["cout"] > 0:
                    object[name]["pts par cout total"] = round(object[name]["pts moy total"] / object[name]["cout"], 2)
                else:
                    object[name]["pts par cout total"] = 'Gratuit'

    if action == 'show':
        print('Data des ' + role + 's en ' + ligue)
        print(pd.DataFrame(object).T.sort_values('pts moy total', ascending=False))
        print('\n')
    elif action == 'register':
        os.chdir(data_path)
        os.makedirs('./' + ligue + '/' + role, exist_ok=True)
        pd.DataFrame(object).T.sort_values('pts moy total', ascending=False).to_csv('./' + ligue + '/' + role + '/all.csv',
                                                                                    index=True)


def getStatsByPlayer(role, ligue):
    os.chdir(base_path)
    with open(ligue + '-players.json') as players:
        playersData = json.load(players)
        playersByRole = []
        for player in playersData:
            if player.get('role') == role.upper():
                playersByRole.append(player)

        for player in playersByRole:
            playerNickname = player.get('nickname')
            # print(playerNickname)

            os.chdir(base_path)
            with open('./' + ligue + '-itemsResults2.json') as results:
                roleResult = []
                for result in json.load(results).get(role):
                    if result.get('playerId') == playerNickname:
                        roleResult.append(result.get('items'))
                # print(roleResult)
            with open('./' + ligue + '-items2.json') as items:
                object = {}
                itemsData = json.load(items)
                for item in itemsData:
                    itemId = item.get('id')
                    name = ''
                    for translation in item.get('translations'):
                        if translation.get('locale') == 'fr':
                            name = translation.get('name')
                        elif translation.get('locale') == 'en':
                            en_name = translation.get('name')
                    isValid = sum(x.get(itemId) is not None and x.get(itemId) > 0 for x in roleResult)
                    if isValid > 0:
                        object[name] = {}
                        object[name]['Nom Anglais'] = en_name
                        object[name]["nb games valide"] = isValid
                        object[name]["total games"] = len(roleResult)
                        object[name]["ratio"] = round(sum(x.get(itemId) is not None and x.get(itemId) > 0 for x in roleResult) / len(
                            roleResult), 2)
                        object[name]["%"] = "{:.0%}".format(
                            sum(x.get(itemId) is not None and x.get(itemId) > 0 for x in roleResult) / len(roleResult))
                        total = 0
                        for x in roleResult:
                            if x.get(itemId) is not None and x.get(itemId) > 0:
                                total += x.get(itemId)
                        if sum(x.get(itemId) is not None and x.get(itemId) > 0 for x in roleResult) > 0:
                            object[name]["pts moy"] = round(total / sum(
                                x.get(itemId) is not None and x.get(itemId) > 0 for x in roleResult), 2)
                        else:
                            object[name]["pts moy"] = 0

                        object[name]["pts moy total"] = round(total / len(roleResult), 2)
                        object[name]["total point"] = total
                        object[name]["cout"] = item.get('baseCost')
                        if object[name]["cout"] > 0:
                            object[name]["pts par cout moy"] = round(object[name]["pts moy"] / object[name]["cout"], 2)
                        else:
                            object[name]["pts par cout moy"] = 'Gratuit'

                        if object[name]["cout"] > 0:
                            object[name]["pts par cout total"] = round(object[name]["pts moy total"] / object[name]["cout"], 2)
                        else:
                            object[name]["pts par cout total"] = 'Gratuit'
                        object[name]["pts par cout moy+1"] = round(object[name]["pts moy"] / (object[name]["cout"]+1), 2)
                        object[name]["pts par cout total+1"] = round(object[name]["pts moy total"] / (object[name]["cout"]+1), 2)
            os.chdir(data_path)
            os.makedirs('./' + ligue + '/' + role, exist_ok=True)
            pd.DataFrame(object).T.sort_values('pts moy total', ascending=False).to_csv('./' + ligue + '/' + role + '/' + playerNickname + '.csv',
                                                                                        index=True)

def zip_files(ligue):
    os.chdir(data_path)
    shutil.make_archive(ligue, 'zip', './' + ligue)
    print('Zip créé')
    shutil.move(ligue + '.zip', './' + ligue + '/' + ligue + '.zip')


def release():
    tag = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    os.chdir(data_path)
    os.system('git add .')
    os.system('git commit -m "release"')
    os.system('git pull')
    os.system('git push')
    os.system('git tag ' + tag)
    os.system('git push --tags')
    print('Release terminé')

