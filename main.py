#!/usr/bin/env python
# This is a sample Python script.

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import sys

from controller import getMatchs, getGamesResult, getStats, initData, zip_files, release, getStatsByPlayer, initDataLeague

# def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    # print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


ligues = ['lec', 'lfl', 'superliga']
# roles = ['coach']
roles = ['coach', 'top', 'jungler', 'mid', 'adc', 'support']
cookie = 'OptanonAlertBoxClosed=2023-01-07T13:42:51.273Z; eupubconsent-v2=CPSck6VPSck6VAcABBENCzCgAAAAAAAAAChQAAAAAAAA.YAAAAAAAAAAA; sessionId=s%3AlAC5GuIBrqAnVpb_1Yb1DpNFESxjCy_S.%2BQnljBDgp9qLevc2UC8Jz%2B9jB9q21ZYCz%2FUWHN1S0%2B4; OptanonConsent=isIABGlobal=false&datestamp=Tue+Jan+17+2023+15%3A52%3A39+GMT%2B0100+(heure+normale+d%E2%80%99Europe+centrale)&version=6.12.0&hosts=&consentId=ac144d43-9e8c-4ac7-834d-ea35dd7ad95e&interactionCount=2&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A0%2CC0003%3A0%2CC0004%3A0&geolocation=FR%3BGES&AwaitingReconsent=false'
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
