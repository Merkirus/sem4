from bs4 import BeautifulSoup
import requests, re, os, csv, time

def find_club_name(html):
    # Extract lines between <caption> and caption>
    pattern = r'<caption[^>]*>(.*?)<\/caption>'
    matches = re.findall(pattern, html, re.DOTALL)

    # Remove lines containing 'caption>'
    filtered_lines = [line for line in matches if 'caption>' not in line]

    # Remove duplicates
    unique_lines = list(set(filtered_lines))

    # Remove 'Player' and 'Table' from each line
    processed_lines = [re.sub(r'Player.*Table', '', line) for line in unique_lines]

    return processed_lines[0].rstrip().lstrip()

def get_team_data(table):
    rows = table.find_all('tr') #pyright: ignore

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
        player_data = [column.get_text().rstrip().lstrip() for column in columns]
        player_data[2] = player_data[2].split()[1]
        player_data[4] = player_data[4].split('-')[0]
        data.append(player_data)

    return column_names, data

def get_shot_data(table):
    rows = table.find_all('tr') #pyright: ignore

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
        player_data = [column.get_text().rstrip().lstrip() for column in columns]
        if all(i == '' for i in player_data):
            continue
        data.append(player_data)
    return column_names, data

def write_csv(url):
    code = url.split(r'/')
    code = code[-1]

    folder = './database/' + code

    if not os.path.isdir(folder):
        os.mkdir(folder)

    result = requests.get(url)

    html = result.content

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
    table_1_shots = soup4.find_all('tbody')[1]
    table_2_shots = soup4.find_all('tbody')[2]

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

    with open(f'{folder}/{find_club_name(soup3.prettify())}_shots.csv', 'w+', newline='') as f:
        writer = csv.writer(f)
        column_names, data = get_shot_data(table_2_shots)
        writer.writerow(column_names)
        writer.writerows(data)

if __name__ == "__main__":
    with open('links_man.txt') as f:
        lines = f.readlines()
        for line in lines:
            print(line.rstrip())
            time.sleep(5.0)
            write_csv(line.rstrip())

    # with open('links_inter.txt') as f:
    #     lines = f.readlines()
    #     for line in lines:
            # time.sleep(5.0)
    #         write_csv(line.rstrip())
    #
    # with open('links_milan.txt') as f:
    #     lines = f.readlines()
    #     for line in lines:
            # time.sleep(5.0)
    #         write_csv(line.rstrip())
    #
    # with open('links_real.txt') as f:
    #     lines = f.readlines()
    #     for line in lines:
            # time.sleep(5.0)
    #         write_csv(line.rstrip())
