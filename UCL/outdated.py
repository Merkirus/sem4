from bs4 import BeautifulSoup
import requests, re, os

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

def extract_shot_table(html, team):

    content = html.split('\n')
    club_shots = ""
    club_shots = ""
    counter = 1 + team
    it = 0
    for line in content:
        if "div_shots" in line:
            it += 1
        if counter == it:
            club_shots += line.rstrip()
            club_shots += '\n'
    return club_shots.rstrip()

def players_to_csv(html):
    output_string = re.sub(r'<thead>.*?</thead>', '', html, flags=re.DOTALL)
    return output_string

def shots_to_csv(html):
    result = ""
    return result

def make_entry(url):

    code = url.split(r'/')
    code = code[-1]

    folder = './' + code

    os.mkdir(folder)

    result = requests.get(url)

    html = result.content

    soup = BeautifulSoup(html, features='html.parser')

    table_div = soup.find_all('div', id=re.compile(r'^switcher_player_stats_'))
    team1 = table_div[0]
    team2 = table_div[1]
    soup2 = BeautifulSoup(str(team1), features='html.parser')
    soup3 = BeautifulSoup(str(team2), features='html.parser')

    club_name1 = find_club_name(soup2.prettify())
    club_name2 = find_club_name(soup3.prettify())

    table_div2 = soup.find('div', id=re.compile(r'^switcher_shots'))
    soup4 = BeautifulSoup(str(table_div2), features='html.parser')

    club_name1_shots = extract_shot_table(soup4.prettify(), 1)
    club_name2_shots = extract_shot_table(soup4.prettify(), 2)

    with open(f"{folder}/{club_name1}", "w+") as f:
        f.write(soup2.prettify())
        f.write(club_name1_shots)

    with open(f"{folder}/{club_name2}", "w+") as f:
        f.write(soup3.prettify())
        f.write(club_name2_shots)

