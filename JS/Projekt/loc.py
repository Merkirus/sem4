import pycurl
import json
from io import BytesIO
import os, sys
import constants

def archive_location(city, path_to_city):
    geo_key = 'pk.96425b92e86eb5121bcf4ee97f40a7a5'
    geo_api = 'https://us1.locationiq.com/v1/search'
    geo_query = f'{geo_api}?key={geo_key}&q={city}&format=json'

    buffer = BytesIO()
    c = pycurl.Curl()
    c.setopt(pycurl.URL, geo_query)
    c.setopt(pycurl.WRITEDATA, buffer)
    c.perform()
    c.close()

    body = buffer.getvalue()
    body = body.decode('iso-8859-1')

    body_json = json.loads(body)
    
    if type(body_json) == dict and body_json.get('error', None):
        return constants.Error.LOCATION

    with open(path_to_city, 'w+') as f:
        json.dump(body_json, f)

def get_location(city):
    if not os.path.isdir(constants.Database.LOCATION.value):
        os.mkdir(constants.Database.LOCATION.value)

    path_to_city = f'{constants.Database.LOCATION.value}/{city}.json'

    def get_lon_lat(path):
        lon = ''
        lat = ''
        with open(path, 'r') as f:
            data = json.load(f)
            if len(data) != 0:
                lon = data[0]['lon']
                lat = data[0]['lat']
        return lon, lat

    if os.path.exists(path_to_city):
        return get_lon_lat(path_to_city)
    else:
        archive_result = archive_location(city, path_to_city)
        if archive_result:
            return archive_result
        return get_lon_lat(path_to_city)

if __name__ == "__main__":
    args = sys.argv[1:]

    if len(args) != 1:
        exit(1)

    city = args[0]

    get_location(city)

