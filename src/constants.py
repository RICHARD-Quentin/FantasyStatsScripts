import os

# Constants for the roles
TOP = 0
JUNGLE = 1
MID = 2
ADC = 3
SUPP = 4
COACH = 5

project_path = '~/Documents/FantasyStatsScripts'
base_path = os.path.expanduser(project_path)

# Path to the folder where finals the data will be stored
data_path = os.path.join(base_path, 'FantasyStats')

# Path to the folder where the data of each league will be stored ( items, players, teams, etc.)
lec_path = os.path.join(base_path, 'data', 'lec')
lfl_path = os.path.join(base_path, 'data', 'lfl')
superliga_path = os.path.join(base_path, 'data', 'superliga')

# Path to the folder where the data of each league will be stored ( items, players, teams, etc.)
data_ligues_path = {
    'lec': lec_path,
    'lfl': lfl_path,
    'superliga': superliga_path
}

ligues = ['lec', 'lfl', 'superliga']
roles = ['coach', 'top', 'jungler', 'mid', 'adc', 'support']
cookie = 'OptanonAlertBoxClosed=2023-01-07T13:42:51.273Z; eupubconsent-v2=CPSck6VPSck6VAcABBENCzCgAAAAAAAAAChQAAAAAAAA.YAAAAAAAAAAA; sessionId=s%3AlAC5GuIBrqAnVpb_1Yb1DpNFESxjCy_S.%2BQnljBDgp9qLevc2UC8Jz%2B9jB9q21ZYCz%2FUWHN1S0%2B4; OptanonConsent=isIABGlobal=false&datestamp=Tue+Jan+17+2023+15%3A52%3A39+GMT%2B0100+(heure+normale+d%E2%80%99Europe+centrale)&version=6.12.0&hosts=&consentId=ac144d43-9e8c-4ac7-834d-ea35dd7ad95e&interactionCount=2&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A0%2CC0003%3A0%2CC0004%3A0&geolocation=FR%3BGES&AwaitingReconsent=false'
args = ['init', 'release', 'autorelease', 'check']

ligues_headers = {
    'lfl': {
        'cookie': cookie.replace(u"\u2018", "'").replace(u"\u2019", "'"),
        'origin': 'https://lfl.superfantasylol.com',
        'referer': 'https://lfl.superfantasylol.com',
        'content-language': 'fr'
    },
    'lec': {
        'cookie': cookie.replace(u"\u2018", "'").replace(u"\u2019", "'"),
        'origin': 'https://lec.superfantasylol.com',
        'referer': 'https://lec.superfantasylol.com',
        'content-language': 'fr'
    },
    'superliga': {
        'cookie': cookie.replace(u"\u2018", "'").replace(u"\u2019", "'"),
        'origin': 'https://lvp.superfantasylol.com',
        'referer': 'https://lvp.superfantasylol.com',
        'content-language': 'fr'
    }
}