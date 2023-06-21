import os
import datetime
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from collections import defaultdict

CLUBS = [
    'Manchester City',
    'Real Madrid',
    'Milan',
    'Inter',
    'UCL/Manchester City',
    'UCL/Real Madrid']


def get_player_stat_dict(key, player_data):
    players = defaultdict(lambda: [])
    for player_sheet in player_data:
        for player in player_sheet['player'].values:
            if player_sheet[player_sheet['player'] == player]['position'].iloc[0] == 'GK' or int(
                    player_sheet[player_sheet['player'] == player]['minutes'].iloc[0]) < 10:
                continue
            players[player].append(
                player_sheet[player_sheet['player'] == player][key])

    temp_players = {}
    for k, v in players.items():
        temp_players[k] = (np.sum(v), len(v))

    return temp_players


def get_data(club):
    main_folder = club
    paths_to_files = []

    for fol in os.listdir(main_folder):
        date = fol.split('-')[-5:-2]
        for file in os.listdir(f'{main_folder}/{fol}'):
            if file == club + '.csv' or file == club + '_shots.csv':
                paths_to_files.append(
                    (f'{main_folder}/{fol}/{file}',
                     datetime.datetime.strptime(
                         '-'.join(date),
                         "%B-%d-%Y")))

    paths_to_files = sorted(paths_to_files, key=lambda x: x[0])
    paths_to_files = sorted(paths_to_files, key=lambda x: x[1])
    return paths_to_files


def get_player_data(club):
    paths_to_files = get_data(club)
    player_stats = paths_to_files[::2]
    player_data = [pd.read_csv(file[0]) for file in player_stats]
    return player_data


def get_shot_data(club):
    paths_to_files = get_data(club)
    shot_stats = paths_to_files[1::2]
    shot_data = [pd.read_csv(file[0]) for file in shot_stats]
    return shot_data


if __name__ == "__main__":

    for club in CLUBS:
        player_data = get_player_data(club)
        shot_data = get_shot_data(club)

        goals = []
        for shot_sheet in shot_data:
            goals.append(len(shot_sheet[shot_sheet['outcome'] == 'Goal']))

        xgl = []
        for shot_sheet in shot_data:
            sum = np.sum(shot_sheet['xg_shot'].values)
            xgl.append(sum)

        players_xgl = get_player_stat_dict('xg', player_data)

        os_x = np.linspace(
            start=1,
            stop=len(player_data),
            num=len(player_data))

        plt.plot(
            os_x,
            goals,
            '.',
            marker='o',
            color='tab:blue',
            label="strzelone")
        plt.plot(os_x, goals, color='tab:blue')
        plt.plot(
            os_x,
            xgl,
            '.',
            marker='o',
            color='tab:orange',
            label='oczekiwane')
        plt.plot(os_x, xgl, color='tab:orange')
        plt.ylabel('Gole')
        plt.xlabel('Mecze kolejki')
        plt.legend(fontsize=12, shadow=True, loc='upper left')
        plt.show()

        players_xgl_assists = get_player_stat_dict('xg_assist', player_data)
        players_sca = get_player_stat_dict('sca', player_data)
        players_gca = get_player_stat_dict('gca', player_data)

        matches_played = [value[1] for value in players_xgl.values()]
        xgl = [value[0] for value in players_xgl.values()]
        xgl_assists = [value[0] for value in players_xgl_assists.values()]
        sca = [value[0] for value in players_sca.values()]
        gca = [value[0] for value in players_gca.values()]

        y_pos = range(len(players_xgl.keys()))

        plt.xticks(y_pos, players_xgl.keys(), rotation=90)
        plt.plot(y_pos, matches_played, label='mecze rozegrane')
        plt.plot(y_pos, xgl, label='gole oczekiwane')
        plt.plot(y_pos, xgl_assists, label='gole oczekiwane po asyście')
        plt.plot(y_pos, gca, label='akcje kreujące gol')
        plt.legend(fontsize=12, shadow=True, loc='upper right')
        plt.show()

        players_passes_completed = get_player_stat_dict(
            'passes_completed', player_data)
        players_passes = get_player_stat_dict('passes', player_data)

        passes_completed = [value[0] / value[1]
                            for value in players_passes_completed.values()]
        passes = [value[0] / value[1] for value in players_passes.values()]

        plt.xticks(y_pos, players_xgl.keys(), rotation=90)
        plt.plot(y_pos, passes_completed, label='śr. udane podania na mecz')
        plt.plot(y_pos, passes, label='śr. podania na mecz')
        plt.legend(fontsize=12, shadow=True, loc='upper right')
        plt.show()
