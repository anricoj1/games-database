import pandas as pd
import numpy as np
import math

def main():
    colnames = ['QueryID', 'ResponseID', 'ResponseName', 'ReleaseDate', 'RecommendationCount', 'SteamSpyOwners', 'PlayersEstimate', 'ControllerSupport', 'IsFree', 'FreeVerAvail', 'PurchaseAvail', 'PlatformWindows', 'PlatformLinux', 'PlatformMac', 'SinglePlayer', 'Multiplayer', 'Coop', 'mmo', 'inApp', 'vrSupport', 'indies', 'action', 'adven', 'casual', 'strat', 'rpg', 'simulation', 'early', 'f2p', 'sports', 'racing', 'mass', 'curren', 'inital', 'final']
    data = pd.read_csv('outfile2.csv', names=colnames, sep=' ')
    print(data.head())

main()
