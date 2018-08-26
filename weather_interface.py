# Author: Karan Chawla (@karanchawla)
# Date: 23rd Aug '18

import datetime
import urllib
import re
import json 
import time 
from slackclient import SlackClient 


class Weather():
    '''
    Uses the open weather api to get the latest weather for the city provided. 
    For more information: https://openweathermap.org
    '''
    def __init__(self, api_key, city_id):
        self._apiKey = api_key
        self._cityId = city_id

    def _time_converter(self, time):
        converted_time = datetime.datetime.fromtimestamp(
            int(time)).strftime('%I:%M %p')
        return converted_time

    def _url_builder(self):
        unit = 'metric'
        api = 'http://api.openweathermap.org/data/2.5/weather?id='
        full_api_url = api + str(self._cityId) + '&mode=json&units=' + unit + '&APPID=' + self._apiKey
        return full_api_url

    def data_fetch(self, full_api_url):
        url = urllib.request.urlopen(full_api_url)
        output = url.read().decode('utf-8')
        self._rawApiDict = json.loads(output)
        url.close()

    def data_organizer(self):
        data = dict(
        city = self._rawApiDict.get('name'),
        country = self._rawApiDict.get('sys').get('country'),
        temp = self._rawApiDict.get('main').get('temp'),
        temp_max = self._rawApiDict.get('main').get('temp_max'),
        temp_min = self._rawApiDict.get('main').get('temp_min'),
        humidity = self._rawApiDict.get('main').get('humidity'),
        pressure = self._rawApiDict.get('main').get('pressure'),
        sky = self._rawApiDict['weather'][0]['main'],
        sunrise = self._time_converter(self._rawApiDict.get('sys').get('sunrise')),
        sunset = self._time_converter(self._rawApiDict.get('sys').get('sunset')),
        wind = self._rawApiDict.get('wind').get('speed'),
        wind_deg = self._rawApiDict.get('deg'),
        dt = self._time_converter(self._rawApiDict.get('dt')),
        cloudiness = self._rawApiDict.get('clouds').get('all'))
        return data

    def get_weather_data(self):
        self.data_fetch(self._url_builder())
        return self.data_organizer()