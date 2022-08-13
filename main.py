#!/usr/bin/env python
# This is a sample Python script.

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import sys

from controller import getMatchs, getGamesResult, getStats, initData, initItems, zip_files, release, getStatsByPlayer, \
    initDataLeague


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


ligues = ['lec', 'lfl']
# roles = ['coach']
roles = ['coach', 'top', 'jungler', 'mid', 'adc', 'support']
cookie = 'OptanonAlertBoxClosed=2022-01-07T13:07:27.016Z; eupubconsent-v2=CPSck6VPSck6VAcABBENCSCgAAAAAAAAAChQAAAAAAAA.YAAAAAAAAAAA; sessionId=s%3AWKXGZ4FmXsQg5zXuJmpNaCe1ni3siapw.NwqG7MgUtZtTdGP5UP0fC8tJuFQdDJ0SdCl2B6og%2BJY; OptanonConsent=isIABGlobal=false&datestamp=Thu+Jun+09+2022+10%3A40%3A57+GMT%2B0200+(heure+d%E2%80%99%C3%A9t%C3%A9+d%E2%80%99Europe+centrale)&version=6.12.0&hosts=&consentId=ac144d43-9e8c-4ac7-834d-ea35dd7ad95e&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A0%2CC0003%3A0%2CC0004%3A0&geolocation=FR%3BGES&AwaitingReconsent=false'
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    if sys.argv[1] == 'init':
        initData(cookie)
        # for ligue in ligues:
        #     for role in roles:
        #         getStats(role, ligue, 'register')

    if sys.argv[1] == 'release':
        # initData(cookie)
        if len(sys.argv) > 2:
            ligues = [sys.argv[2]]
        for ligue in ligues:
            initDataLeague(cookie, ligue)
            for role in roles:
                getStats(role, ligue, 'register')
                getStatsByPlayer(role, ligue)
            zip_files(ligue)
        release()
    else:
        ligue = sys.argv[1]
        if ligue in ligues:
            for role in roles:
                getStats(role, ligue, 'show')

    # See PyCharm help at https://www.jetbrains.com/help/pycharm/
