#/bin/python3
import json
import os
import shutil
from datetime import datetime
import requests
import pandas as pd
import asyncio
import aiohttp
import itertools
import time
import logging

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

logging.basicConfig(filename=f'{base_path}/fantasy.log', filemode='a', format='%(asctime)s - %(message)s', level=logging.DEBUG)


def initData(cookie):
    ligues = ['lec', 'lfl', 'superliga']

    for ligue in ligues:
        getItems(ligue, cookie)
        getPlayers(ligue, cookie)
        getMatchs(ligue, cookie)
        # getGamesResult(ligue, cookie)
        asyncio.run(get_game_result(ligue, cookie))

def initDataLeague(cookie, ligue):
    try:
        print('Importation des données pour la ligue : ' + ligue)
        logging.info('Importation des données pour la ligue : ' + ligue)
        getItems(ligue, cookie)
        getPlayers(ligue, cookie)
        getMatchs(ligue, cookie)
        # getGamesResult(ligue, cookie)
        asyncio.run(get_game_result(ligue, cookie))
    except Exception as e:
        print(e)
        logging.error(e)

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

async def fetch_game_result(session, ligue, cookie, id):
    if ligue == 'superliga':
        url = f'https://api-{ligue}.superfantasylol.com/api/v1/games/{id}'
        headers = {
            'cookie': cookie.replace(u"\u2018", "'").replace(u"\u2019", "'"),
            'origin': f'https://lvp.superfantasylol.com',
            'referer': f'https://lvp.superfantasylol.com/',
            'content-language': 'fr'
        }
    else:
        url = f'https://api-{ligue}.superfantasylol.com/api/v1/games/{id}'
        headers = {
            'cookie': cookie.replace(u"\u2018", "'").replace(u"\u2019", "'"),
            'origin': f'https://{ligue}.superfantasylol.com',
            'referer': f'https://{ligue}.superfantasylol.com/',
            'content-language': 'fr'
        }

    async with session.get(url, headers=headers) as response:
        result = await response.json()
        data = result.get('data')
        if data is not None:
            local = data.get('local').get('team').get('shortName')
            visitor = data.get('visitor').get('team').get('shortName')
            local_players = data.get('local').get('players')
            visitor_players = data.get('visitor').get('players')
            print_message = f'{local} - {visitor}'
            top = [
                {
                    'playerId': local_players[TOP].get('player').get('nickname'),
                    'items': local_players[TOP].get('items')
                },
                {
                    'playerId': visitor_players[TOP].get('player').get('nickname'),
                    'items': visitor_players[TOP].get('items')
                }
            ]
            jungler = [
                {
                    'playerId': local_players[JUNGLE].get('player').get('nickname'),
                    'items': local_players[JUNGLE].get('items')
                },
                {
                    'playerId': visitor_players[JUNGLE].get('player').get('nickname'),
                    'items': visitor_players[JUNGLE].get('items')
                }
            ]
            mid = [
                {
                    'playerId': local_players[MID].get('player').get('nickname'),
                    'items': local_players[MID].get('items')
                },
                {
                    'playerId': visitor_players[MID].get('player').get('nickname'),
                    'items': visitor_players[MID].get('items')
                }
            ]
            adc = [
                {
                    'playerId': local_players[ADC].get('player').get('nickname'),
                    'items': local_players[ADC].get('items')
                },
                {
                    'playerId': visitor_players[ADC].get('player').get('nickname'),
                    'items': visitor_players[ADC].get('items')
                }
            ]
            support = [
                {
                    'playerId': local_players[SUPP].get('player').get('nickname'),
                    'items': local_players[SUPP].get('items')
                },
                {
                    'playerId': visitor_players[SUPP].get('player').get('nickname'),
                    'items': visitor_players[SUPP].get('items')
                }
            ]
            coach = [
                {
                    'playerId': local_players[COACH].get('player').get('nickname'),
                    'items': local_players[COACH].get('items')
                },
                {
                    'playerId': visitor_players[COACH].get('player').get('nickname'),
                    'items': visitor_players[COACH].get('items')
                }
            ]
            print(f'Import game {print_message} terminé')
            return {
                'top': top,
                'jungler': jungler,
                'mid': mid,
                'adc': adc,
                'support': support,
                'coach': coach
            }
        else:
            return None

async def get_game_result(ligue, cookie):
    os.chdir(base_path)
    with open(f'{ligue}-matchs.json') as data:
        matchesId = json.load(data)
    
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_game_result(session, ligue, cookie, id) for id in matchesId]
        results = await asyncio.gather(*tasks)

        top = list(itertools.chain.from_iterable([result.get('top') for result in results if result is not None]))
        jungler = list(itertools.chain.from_iterable([result.get('jungler') for result in results if result is not None]))
        mid = list(itertools.chain.from_iterable([result.get('mid') for result in results if result is not None]))
        adc = list(itertools.chain.from_iterable([result.get('adc') for result in results if result is not None]))
        support = list(itertools.chain.from_iterable([result.get('support') for result in results if result is not None]))
        coach = list(itertools.chain.from_iterable([result.get('coach') for result in results if result is not None]))

    result = {
        'top': top,
        'jungler': jungler,
        'mid': mid,
        'adc': adc,
        'support': support,
        'coach': coach
    }
    with open(f'{ligue}-itemsResults2.json', 'w+') as results_file:
        json.dump(result, results_file, default=str)

    print(f'Games results {ligue} importés')


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
                object[name]["pts par cout moy+1"] = round(object[name]["pts moy"] / (object[name]["cout"]+1), 2)
                object[name]["pts par cout total+1"] = round(object[name]["pts moy total"] / (object[name]["cout"]+1), 2)

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
    logging.info('zip créé')
    print('Zip créé')
    shutil.move(ligue + '.zip', './' + ligue + '/' + ligue + '.zip')


def release(ligue):
    tag = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    os.chdir(data_path)
    os.system(f'git add {ligue}')
    os.system(f'git commit -m "release {ligue}"')
    os.system('git pull')
    os.system('git push')
    os.system('git tag ' + tag)
    os.system('git push --tags')
    logging.info('release ' + ligue + ' terminé')
    print(f'Release {ligue} terminé')            



def release_ligue(ligue, roles, cookie):
    try:
        logging.info('release ligue ' + ligue)
        initDataLeague(cookie, ligue)
        for role in roles:
            getStats(role, ligue, 'register')
            getStatsByPlayer(role, ligue)
        zip_files(ligue)
        release(ligue)
    except Exception as e:
        logging.error('release ' + ligue + ' échoué')
        logging.error(e)

def auto_release_ligue(ligues, roles, cookie):
    checkRelease = True
    counter = 1
    logging.info('auto release')
    isFinished = {key: False for key in ligues}
    while(checkRelease and counter <= 9):
        logging.info('check release n°' + str(counter))
        logging.info('isFinished ' + str(isFinished))
        for ligue in ligues:
            if isFinished[ligue]:
                continue
            result = check_end_gameday(ligue, cookie)
            logging.debug(ligue + ' ' + str(result))
            if result['matchDay'] and result['dayFinished']:
                release_ligue(ligue, roles, cookie)
                isFinished[ligue] = True
            if not result['matchDay']:
                isFinished[ligue] = True
        logging.debug('isFinished ' + str(isFinished))
        logging.debug('allFinished ' + str(all(isFinished.values())))
        checkRelease = not all(isFinished.values())
        counter += 1
        logging.info('check release n°' + str(counter) + ' : ' + str(checkRelease))
        time.sleep(30)

def check_end_gameday(ligue, cookie):
    if ligue == 'superliga':
        headersLeague= 'lvp'
    else :
        headersLeague= ligue
    url = f'https://api-{ligue}.superfantasylol.com/api/v1/gamedays'
    headers={
    'cookie': cookie.replace(u"\u2018", "'").replace(u"\u2019", "'"),
    'origin': f'https://{headersLeague}.superfantasylol.com',
    'referer': f'https://{headersLeague}.superfantasylol.com',
    'content-language': 'fr'
}
    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        gamedays = r.json()["data"]
    except requests.exceptions.HTTPError as err:
        logging.error(err)
        print(err)
        return False
    
    logging.info('Check end gameday ' + ligue)
    print('Check end gameday', ligue)
    today = datetime.today()
    result = {
        'matchDay': False,
        'dayFinished': False
    }
    for gameday in gamedays:
        matches = gameday.get('matches')
        if not matches:
            continue
        last_match_date = datetime.strptime(matches[-1].get('date'), '%Y-%m-%dT%H:%M:%S.%fZ')
        if last_match_date.date().strftime("%Y-%m-%d") == today.date().strftime("%Y-%m-%d"): 
            todaygames = gameday
            print('Matchs a jouer :')
            logging.info('Matchs a jouer :')
            for match in todaygames.get('matches'):
                print(match.get('date'), ' - ', match.get('local').get('name'), ' - ' , match.get('visitor').get('name'), ' - ', match.get('status'))
                logging.info(match.get('date') + ' - ' + match.get('local').get('name') + ' - ' + match.get('visitor').get('name') + ' - ' + match.get('status'))
                if match.get('status') != 'COMPUTED':
                    print('Il reste des matchs à jouer')
                    logging.info('Il reste des matchs à jouer')
                    result['matchDay'] = True
                    result['dayFinished'] = False
                    return result
            print('Tous les matchs sont terminés')
            logging.info('Tous les matchs sont terminés')
            result['matchDay'] = True
            result['dayFinished'] = True
            return result
    print('Aucun match n\'est prévu aujourd\'hui')
    logging.info('Aucun match n\'est prévu aujourd\'hui')
    result['matchDay'] = False
    result['dayFinished'] = False
    return result