import requests
import os
import duckdb

from functools import lru_cache
from pyzipcode import ZipCodeDatabase
from tempfile import NamedTemporaryFile


OPEN_WEATHER_MAP_KEY = os.getenv('OPEN_WEATHER_MAP_KEY')


def weather(*, zip_code: str, units: str = 'imperial'):
    # TODO(marcua): Internationalize.
    zcdb = ZipCodeDatabase()
    code = zcdb[zip_code]
    lat: float = code.latitude
    lon: float = code.longitude
    response = requests.get(
        f'https://api.openweathermap.org/data/2.5/onecall?'
        f'lat={lat}'
        f'&lon={lon}'
        f'&units={units}'
        f'&appid={OPEN_WEATHER_MAP_KEY}')
    results = response.json()
    today = results['daily'][0]
    descriptions = ', '.join(
        entry['description'] for entry in today['weather'])
    results['today'] = {
        'morning': {
            'temp': today['temp']['morn'],
            'feels_like': today['feels_like']['morn']
        },
        'day': {
            'temp': today['temp']['day'],
            'feels_like': today['feels_like']['day']
        },
        'evening': {
            'temp': today['temp']['eve'],
            'feels_like': today['feels_like']['eve']
        },
        'night': {
            'temp': today['temp']['night'],
            'feels_like': today['feels_like']['night']
        },
        'uvi': today['uvi'],
        'description': descriptions}
    return results


@lru_cache(maxsize=None)
def _nyt_covid_relation():
    with NamedTemporaryFile(delete=False) as csv_file:
        csv_file.write(requests.get(
            'https://raw.githubusercontent.com/nytimes/covid-19-data/'
            'master/rolling-averages/us-counties-recent.csv').content)
        csv_file.flush()
        relation = duckdb.from_csv_auto(csv_file.name)
        return relation


def nyt_covid(*, state: str, county: str):
    relation = _nyt_covid_relation()
    result = relation.query('nyt_county_covid', f'''
        SELECT
            cases_avg_per_100k,
            date
         FROM nyt_county_covid
         WHERE
             state = '{state}'
             AND county = '{county}'
         ORDER BY date DESC
         LIMIT 1;
    ''').fetchone()
    return {'cases_avg_per_100k': result[0], 'date': str(result[1])}
