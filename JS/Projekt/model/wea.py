import pycurl
import json
from io import BytesIO
import os, sys
import loc
import constants

def get_json(query):
    buffer = BytesIO()
    c = pycurl.Curl()
    c.setopt(pycurl.URL, query)
    c.setopt(pycurl.WRITEDATA, buffer)
    c.perform()
    c.close()

    body = buffer.getvalue()
    body = body.decode('iso-8859-1')

    return json.loads(body)

def get_backup_json(main_json, lat, lon, date):
    weather_key = 'df60cbe881324cd4b55170544231606' # free trial expires 30 June 2023
    weather_api = 'http://api.weatherapi.com/v1/history.json'
    query = f'{weather_api}?key={weather_key}&q={lat},{lon}&dt={date}'

    body_json = get_json(query)

    if body_json.get('error', None):
        return constants.Error.WEATHER_API

    weather_info = body_json['forecast']['forecastday'][0]['day']

    main_json['daily']['weathercode'] = [constants.WEATHERCODE.get(str(int(weather_info['condition']['code'][-2:])), constants.Emojis.UNSPECIFIED_WEATHER.value)]
    main_json['daily']['temperature_2m_max'] = [weather_info['maxtemp_c']]
    main_json['daily']['temperature_2m_min'] = [weather_info['mintemp_c']]
    main_json['daily']['temperature_2m_avg'] = [weather_info['avgtemp_c']]
    main_json['daily']['precipitation_sum'] = weather_info['totalprecip_mm']

def get_avg_temp(body_json):
    temps = [float(x) for x in body_json['hourly']['temperature_2m']]

    return round(sum(temps)/len(temps), 1)

def nullable_json(data):
    for _, v in data['daily'].items():
        if None in v:
            return constants.Error.WEATHER_NULL

    for _, v in data['hourly'].items():
        if None in v:
            return constants.Error.WEATHER_NULL

def get_working_json(lat, lon, date):

    apis = [constants.API.ARCHIVE.value, constants.API.FORECAST.value]
    params = 'weathercode,temperature_2m_max,temperature_2m_min,precipitation_sum'
    queries = [f'{apis[0]}?latitude={lat}&longitude={lon}&start_date={date}&end_date={date}&hourly=temperature_2m&daily={params}&timezone=auto',
               f'{apis[1]}?latitude={lat}&longitude={lon}&start_date={date}&end_date={date}&hourly=temperature_2m&daily={params}&timezone=auto']

    body_json = {}

    for query in queries:
        body_json = get_json(query)

        if body_json.get('error', None):
            continue

        if not nullable_json(body_json):
            body_json['daily']['weathercode'] = [constants.WEATHERCODE.get(str(body_json['daily']['weathercode'][0]), constants.Emojis.UNSPECIFIED_WEATHER.value)]
            body_json['daily']['temperature_2m_avg'] = [get_avg_temp(body_json)]

            return body_json
    
    # if body_json.get('error', None):
    #     return constants.Error.WEATHER_API

    backup_result = get_backup_json(body_json, lat, lon, date)
    if backup_result:
        return backup_result

    return body_json

def archive_weather(city, date, path_to_city):
    lon = ''
    lat = ''

    location_result = loc.get_location(city)
    if isinstance(location_result, constants.Error):
        return location_result
    else:
        lon, lat = location_result

    body_json = get_working_json(lat, lon, date)

    if isinstance(body_json, constants.Error):
        return body_json

    with open(path_to_city, 'w+') as f:
        json.dump(body_json, f)

def get_weather(city, date):
    if not os.path.isdir(constants.Database.WEATHER.value):
        os.mkdir(constants.Database.WEATHER.value)

    path_to_city = f'{constants.Database.WEATHER.value}/{city}_{date}.json'

    if os.path.exists(path_to_city):
        with open(path_to_city, 'r') as f:
            return json.load(f)
    else:
        archive_result = archive_weather(city, date, path_to_city)
        if archive_result:
            return archive_result
        with open(path_to_city, 'r') as f:
            return json.load(f)

if __name__ == "__main__":
    args = sys.argv[1:]

    if len(args) != 2:
        exit(1)

    city = args[0]
    date = args[1]

    print(get_weather(city, date))

