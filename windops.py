# Author: Karan Chawla (@karanchawla)
# Date: 23rd Aug '18

import datetime
import urllib.request
import re
import json 
import time 
from slackclient import SlackClient 

# Open Weather Map API 

def time_converter(time):
    converted_time = datetime.datetime.fromtimestamp(
        int(time)
    ).strftime('%I:%M %p')
    return converted_time


def url_builder(city_id):
    user_api = 'your user api key here'  
    unit = 'metric'  # For Fahrenheit use imperial, for Celsius use metric, and the default is Kelvin.
    api = 'http://api.openweathermap.org/data/2.5/weather?id='     # City ID list here: http://bulk.openweathermap.org/sample/city.list.json.gz
    # Hayward: 5355933
    full_api_url = api + str(city_id) + '&mode=json&units=' + unit + '&APPID=' + user_api  
    return full_api_url


def data_fetch(full_api_url):
    url = urllib.request.urlopen(full_api_url)
    output = url.read().decode('utf-8')
    raw_api_dict = json.loads(output)
    url.close()
    return raw_api_dict


def data_organizer(raw_api_dict):
    data = dict(
        city=raw_api_dict.get('name'),
        country=raw_api_dict.get('sys').get('country'),
        temp=raw_api_dict.get('main').get('temp'),
        temp_max=raw_api_dict.get('main').get('temp_max'),
        temp_min=raw_api_dict.get('main').get('temp_min'),
        humidity=raw_api_dict.get('main').get('humidity'),
        pressure=raw_api_dict.get('main').get('pressure'),
        sky=raw_api_dict['weather'][0]['main'],
        sunrise=time_converter(raw_api_dict.get('sys').get('sunrise')),
        sunset=time_converter(raw_api_dict.get('sys').get('sunset')),
        wind=raw_api_dict.get('wind').get('speed'),
        wind_deg=raw_api_dict.get('deg'),
        dt=time_converter(raw_api_dict.get('dt')),
        cloudiness=raw_api_dict.get('clouds').get('all')
    )
    return data


def data_output(data):
    m_symbol = '\xb0' + 'C'
    print('---------------------------------------')
    print('Current weather in: {}, {}:'.format(data['city'], data['country']))
    print(data['temp'], m_symbol, data['sky'])
    print('Max: {}, Min: {}'.format(data['temp_max'], data['temp_min']))
    print('')
    print('Wind Speed: {}, Degree: {}'.format(data['wind'], data['wind_deg']))
    print('Humidity: {}'.format(data['humidity']))
    print('Cloud: {}'.format(data['cloudiness']))
    print('Pressure: {}'.format(data['pressure']))
    print('Sunrise at: {}'.format(data['sunrise']))
    print('Sunset at: {}'.format(data['sunset']))
    print('')
    print('Last update from the server: {}'.format(data['dt']))
    print('---------------------------------------')

slack_client = SlackClient("your slack bot key here")
user_list = slack_client.api_call("users.list")
for user in user_list.get('members'):
    if user.get('name') == "weatherops":
        bot_user_id = user.get('id')
        break 

if slack_client.rtm_connect():
    print("Connected!")

    while True: 
        new_events = slack_client.rtm_read()
        for event in new_events:
            if "type" in event:
                if event['type'] == "message" and "text" in event:
                    message = event['text']
                    ch = event['channel']
                    print(event)
                    if message.startswith("<@%s>" % bot_user_id):
                        # print("Message received: %s" % json.dumps(message, indent=2))

                        message_text = message.split("<@%s>" % bot_user_id)[1].strip()

                        if re.match(r'.*(wind).*', message_text, re.IGNORECASE):
                            data = data_organizer(data_fetch(url_builder(5355933)))
                            slack_client.api_call("chat.postMessage", channel=ch,
                            text = "Current winds are at {} Kts, last updated from the server at {}".format(float(data['wind']) * 1.94384, data['dt']),
                            as_user=True)
                        elif re.match(r'.*(temperature).*', message_text, re.IGNORECASE):
                            data = data_organizer(data_fetch(url_builder(5355933)))
                            slack_client.api_call("chat.postMessage", channel=ch,
                            text = "Current max is at {} C and the min is {} C, last updated from the server at {}".format(float(data['temp_max']), data['temp_min'], data['dt']),
                            as_user=True)
                        elif re.match(r'.*(pressure).*', message_text, re.IGNORECASE):
                            data = data_organizer(data_fetch(url_builder(5355933)))
                            slack_client.api_call("chat.postMessage", channel=ch,
                            text = "Current pressure is at {} hpa".format(float(data['pressure'])),
                            as_user=True)
                        elif re.match(r'.*(humidity).*', message_text, re.IGNORECASE):
                            data = data_organizer(data_fetch(url_builder(5355933)))
                            slack_client.api_call("chat.postMessage", channel=ch,
                            text = "Current humidity is at {} %".format(float(data['humidity'])),
                            as_user=True)
                        else:
                            data = data_organizer(data_fetch(url_builder(5355933)))
                            slack_client.api_call("chat.postMessage", channel=ch,
                            text = "Sorry I don't understand. If you have feature requests please contact @karan",
                            as_user=True)

        time.sleep(1)
else:
    print("Connection Failed, invalid token?")

