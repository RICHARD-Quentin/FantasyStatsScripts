#/bin/python3
import sys
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
import git
from src.constants import base_path, data_path, data_ligues_path, TOP, JUNGLE, MID, ADC, SUPP, COACH, ligues, roles, ligues_headers

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)
logging.basicConfig(filename=f'{base_path}/fantasy.log', filemode='a', format='%(asctime)s - %(message)s', level=logging.DEBUG)

def init():
    global ligues
    if len(sys.argv) > 2:
        ligues = [sys.argv[2]]
    for ligue in ligues: init_data_league(ligue)

def release():
    global ligues
    if len(sys.argv) > 2:
        ligues = [sys.argv[2]]
    for ligue in ligues: release_ligue(ligue, roles)

def autorelease():
    debug = False
    if len(sys.argv) > 2 and sys.argv[2] == 'debug':
        debug = True
    auto_release_ligue(ligues, roles, debug)

def check():
    for ligue in ligues: 
        result = check_end_gameday(ligue)
        print(ligue, result)

def ligue_stats():
    global roles
    if len(sys.argv) > 2:
        roles = [sys.argv[2]]
    for role in roles: get_stats(role, sys.argv[1], 'show')

def init_folders(ligue):
    print(f'Checking folders for ligue : {data_ligues_path.get(ligue)}')
    if not os.path.exists(data_ligues_path.get(ligue)):
        print(f'Creating folder')
        os.makedirs(data_ligues_path.get(ligue))
    else :
        print('Folder already exists')
        
def init_data():
    ligues = ['lec', 'lfl', 'superliga']

    for ligue in ligues:
        init_folders(ligue)
        get_items(ligue)
        get_players(ligue)
        get_matchs(ligue)
        # get_game_result(ligue)
        asyncio.run(get_game_result(ligue))

def init_data_league(ligue):
    try:
        print('Importation des données pour la ligue : ' + ligue)
        logging.info('Importation des données pour la ligue : ' + ligue)
        init_folders(ligue)
        get_items(ligue)
        get_players(ligue)
        get_matchs(ligue)
        # get_game_result(ligue)
        asyncio.run(get_game_result(ligue))
    except Exception as e:
        print(e)
        logging.error(e)

def get_items(ligue):
    url = f'https://api-{ligue}.superfantasylol.com/api/v1/itemcards'
    headers = ligues_headers.get(ligue)
    r = requests.get(url, headers=headers)
    result = json.loads(r.text)

    # ecriture des logs
    path = data_ligues_path.get(ligue)
    os.chdir(path)
    with open('items.json', 'w+') as outfile:
        json.dump(result.get('data'), outfile, default=str)

    print('Items ' + ligue + ' importés')


def get_players(ligue):
    url = f'https://api-{ligue}.superfantasylol.com/api/v1/playerinfos'
    headers = ligues_headers.get(ligue)
    r = requests.get(url, headers=headers)
    result = json.loads(r.text)

    # ecriture des logs
    path = data_ligues_path.get(ligue)
    os.chdir(path)
    with open('players.json', 'w+') as outfile:
        json.dump(result.get('data'), outfile, default=str)

    print('Players ' + ligue + ' importés')


def get_matchs(ligue):
    url = f'https://api-{ligue}.superfantasylol.com/api/v1/gamedays'
    headers = ligues_headers.get(ligue)
    r = requests.get(url, headers=headers)
    result = json.loads(r.text).get('data')
    gamesId = []
    for game in result:
        for match in game.get('matches'):
            if len(match.get('games')) > 0:
                for game in match.get('games'):
                    gamesId.append(game.get('id'))
    gamesId.reverse()

    # #ecriture des logs
    path = data_ligues_path.get(ligue)
    os.chdir(path)
    with open('matchs.json', 'w+') as outfile:
        json.dump(gamesId, outfile, default=str)

    print('Matchs ' + ligue + ' importés')

async def fetch_game_result(session, ligue, id):
    url = f'https://api-{ligue}.superfantasylol.com/api/v1/games/{id}'
    headers = ligues_headers.get(ligue)
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

async def get_game_result(ligue):
    path = data_ligues_path.get(ligue)
    os.chdir(path)
    with open('matchs.json') as data:
        matchesId = json.load(data)
    
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_game_result(session, ligue, id) for id in matchesId]
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
    with open('items-results.json', 'w+') as results_file:
        json.dump(result, results_file, default=str)

    print(f'Games results {ligue} importés')


def get_stats(role, ligue, action):
    path = data_ligues_path.get(ligue)
    os.chdir(path)
    with open('items-results.json') as results:
        roleResult = []
        for result in json.load(results).get(role):
            roleResult.append(result.get('items'))
        # print(roleResult)
    with open('items.json') as items:
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


def get_stats_by_player(role, ligue):
    path = data_ligues_path.get(ligue)
    os.chdir(path)
    with open('players.json') as players:
        playersData = json.load(players)
        playersByRole = []
        for player in playersData:
            if player.get('role') == role.upper():
                playersByRole.append(player)

        for player in playersByRole:
            playerNickname = player.get('nickname')
            # print(playerNickname)

            os.chdir(path)
            with open('items_results.json') as results:
                roleResult = []
                for result in json.load(results).get(role):
                    if result.get('playerId') == playerNickname:
                        roleResult.append(result.get('items'))
                # print(roleResult)
            with open('items.json') as items:
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
    logging.info(f"Starting release {ligue}")
    print(f"Starting release {ligue}")
    tag = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    repo = git.Repo(data_path)
    repo.config_writer().set_value("user", "name", "RICHARD-Quentin")
    repo.git.add(ligue)
    repo.index.commit(f"release {ligue}")
    repo.remotes.origin.pull()
    repo.remotes.origin.push()
    tag = repo.create_tag(f"release-{ligue}-{datetime.now().strftime('%Y%m%d-%H%M%S')}")
    repo.remotes.origin.push(tag)
    logging.info('release ' + ligue + ' terminé')
    print(f'Release {ligue} terminé')            


def release_ligue(ligue, roles):
    try:
        logging.info('release ligue ' + ligue)
        init_data_league(ligue)
        for role in roles:
            get_stats(role, ligue, 'register')
            get_stats_by_player(role, ligue)
        zip_files(ligue)
        release(ligue)
    except Exception as e:
        logging.error('release ' + ligue + ' échoué')
        logging.error(e)

def auto_release_ligue(ligues, roles, debug):
    checkRelease = True
    counter = 1
    logging.info('auto release')
    isFinished = {key: False for key in ligues}
    while(checkRelease and counter <= 9):
        logging.info('check release n°' + str(counter))
        logging.info('isFinished ' + str(isFinished))
        for ligue in ligues:
            if debug:
                release_ligue(ligue, roles)
                break
            if isFinished[ligue]:
                continue
            result = check_end_gameday(ligue)
            logging.debug(ligue + ' ' + str(result))

            if result['matchDay'] and result['dayFinished']:
                release_ligue(ligue, roles)
                isFinished[ligue] = True
            if not result['matchDay']:
                isFinished[ligue] = True
        logging.debug('isFinished ' + str(isFinished))
        logging.debug('allFinished ' + str(all(isFinished.values())))
        checkRelease = not all(isFinished.values())
        counter += 1
        logging.info('check release n°' + str(counter) + ' : ' + str(checkRelease))
        time.sleep(600)
        if debug:
            break

def check_end_gameday(ligue):
    url = f'https://api-{ligue}.superfantasylol.com/api/v1/gamedays'
    headers = ligues_headers.get(ligue)
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