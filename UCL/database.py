from bs4 import BeautifulSoup
import requests
import re
import os
import csv
import time

# function to get club names from given html, basically striping down html


def find_club_name(html):
    pattern = r'<caption[^>]*>(.*?)<\/caption>'
    matches = re.findall(pattern, html, re.DOTALL)

    filtered_lines = [line for line in matches if 'caption>' not in line]

    unique_lines = list(set(filtered_lines))

    processed_lines = [re.sub(r'Player.*Table', '', line)
                       for line in unique_lines]

    return processed_lines[0].rstrip().lstrip()


def get_team_data(table):
    # tr is one entry in given table
    rows = table.find_all('tr')  # pyright: ignore

    data = []

    column_names = []
    get_column_names = False

    for row in rows:
        # column values can be stored in either th or td
        columns = row.find_all('th')
        columns += row.find_all('td')
        # getting column names stored in data-stat
        if not get_column_names:
            for column in columns:
                column_names.append(column['data-stat'])
            get_column_names = True
        player_data = [column.get_text().rstrip().lstrip()
                       for column in columns]
        if player_data[2]:  # sometimes player country can be missing, doesnt really matter
            player_data[2] = player_data[2].split()[1]  # formatting
        player_data[4] = player_data[4].split('-')[0]  # formatting
        data.append(player_data)

    return column_names, data

# almost same as above with slightly different formatting


def get_shot_data(table):
    rows = table.find_all('tr')  # pyright: ignore

    data = []

    column_names = []
    get_column_names = False

    for row in rows:
        columns = row.find_all('th')
        columns += row.find_all('td')
        if not get_column_names:
            for column in columns:
                column_names.append(column['data-stat'])
            get_column_names = True
        player_data = [column.get_text().rstrip().lstrip()
                       for column in columns]
        if all(i == '' for i in player_data):
            continue
        data.append(player_data)
    return column_names, data

# getting html content, scrapping it and saving to database as csv


def write_csv(url):
    code = url.split(r'/')
    code = code[-1]

    folder = './database/' + code

    if not os.path.isdir(folder):
        os.mkdir(folder)

    result = requests.get(url)

    html = result.content

    # using bs4 as html parser
    soup = BeautifulSoup(html, features='html.parser')

    table_div = soup.find_all('div', id=re.compile(r'^switcher_player_stats_'))

    team1 = table_div[0]
    team2 = table_div[1]
    soup2 = BeautifulSoup(str(team1), features='html.parser')
    soup3 = BeautifulSoup(str(team2), features='html.parser')

    table_div2 = soup.find('div', id=re.compile(r'^switcher_shots'))
    soup4 = BeautifulSoup(str(table_div2), features='html.parser')

    table_1 = soup2.find('tbody')
    table_2 = soup3.find('tbody')
    # index 0 is for universal sheet
    table_1_shots = soup4.find_all('tbody')[1]
    table_2_shots = None  # sometimes second shot sheet is missing
    try:
        table_2_shots = soup4.find_all('tbody')[2]
    except BaseException:
        table_2_shots = None

    with open(f'{folder}/{find_club_name(soup2.prettify())}.csv', 'w+', newline='') as f:
        writer = csv.writer(f)
        column_names, data = get_team_data(table_1)
        writer.writerow(column_names)
        writer.writerows(data)

    with open(f'{folder}/{find_club_name(soup3.prettify())}.csv', 'w+', newline='') as f:
        writer = csv.writer(f)
        column_names, data = get_team_data(table_2)
        writer.writerow(column_names)
        writer.writerows(data)

    with open(f'{folder}/{find_club_name(soup2.prettify())}_shots.csv', 'w+', newline='') as f:
        writer = csv.writer(f)
        column_names, data = get_shot_data(table_1_shots)
        writer.writerow(column_names)
        writer.writerows(data)

    if table_2_shots:
        with open(f'{folder}/{find_club_name(soup3.prettify())}_shots.csv', 'w+', newline='') as f:
            writer = csv.writer(f)
            column_names, data = get_shot_data(table_2_shots)
            writer.writerow(column_names)
            writer.writerows(data)


if __name__ == "__main__":

    if not os.path.isdir('./database'):
        os.mkdir('./database')

    with open('links/links_man.txt') as f:
        lines = f.readlines()
        for line in lines:
            print(line.rstrip())
            # sleeping cause getting banned if more than 20 requests per minute
            time.sleep(5.0)
            write_csv(line.rstrip())

    with open('links/links_inter.txt') as f:
        lines = f.readlines()
        for line in lines:
            print(line.rstrip())
            time.sleep(5.0)
            write_csv(line.rstrip())

    with open('links/links_milan.txt') as f:
        lines = f.readlines()
        for line in lines:
            print(line.rstrip())
            time.sleep(5.0)
            write_csv(line.rstrip())

    with open('links/links_real.txt') as f:
        lines = f.readlines()
        for line in lines:
            print(line.rstrip())
            time.sleep(5.0)
            write_csv(line.rstrip())

    with open('links/links_ucl.txt') as f:
        lines = f.readlines()
        for line in lines:
            print(line.rstrip())
            time.sleep(5.0)
            write_csv(line.rstrip())
