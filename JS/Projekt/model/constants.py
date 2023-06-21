from enum import Enum
from emoji import emojize

class Error(Enum):
    LOCATION = 1
    WEATHER_NULL = 2
    WEATHER_API = 3

class Database(Enum):
    LOCATION = 'location'
    WEATHER = 'weather'

class API(Enum):
    ARCHIVE = 'https://archive-api.open-meteo.com/v1/archive'
    FORECAST = 'https://api.open-meteo.com/v1/forecast'
    BACKUP = 'http://api.weatherapi.com/v1/history.json'

class Emojis(Enum):
    SUN = emojize(':sun:')
    CLOUDY_SUNNY = emojize(':sun_behind_cloud:')
    CLOUDY = emojize(':cloud:')
    FOG = emojize(':fog:')
    WINDY = emojize(':wind_face:')
    RAINY = emojize(':cloud_with_rain:')
    FREEZING_RAINY = emojize(':cloud_with_rain:')+emojize(':snowflake:')
    SNOWY = emojize(':cloud_with_snow:')
    THUNDER = emojize(':cloud_with_lightning:')
    RAINY_THUNDER = emojize(':cloud_with_lightning_and_rain:')
    UNSPECIFIED_WEATHER = emojize(':exclamation_question_mark:')

class Server(Enum):
    URL = '127.0.0.1'
    PORT = '8000'

WEATHERCODE = {
        '0': Emojis.SUN.value,
        '1': Emojis.CLOUDY_SUNNY.value,
        '3': Emojis.CLOUDY.value,
        '10': Emojis.FOG.value,
        '14': Emojis.CLOUDY.value,
        '18': Emojis.WINDY.value,
        '30': Emojis.FOG.value,
        '50': Emojis.RAINY.value,
        '60': Emojis.RAINY.value,
        '63': Emojis.RAINY.value,
        '65': Emojis.FREEZING_RAINY.value,
        '70': Emojis.SNOWY.value,
        '75': Emojis.SNOWY.value,
        '81': Emojis.RAINY.value,
        '83': Emojis.RAINY.value,
        '85': Emojis.SNOWY.value,
        '87': Emojis.SNOWY.value,
        '89': Emojis.SNOWY.value,
        '90': Emojis.THUNDER.value,
        '95': Emojis.RAINY_THUNDER.value
        }

