# Author: Karan Chawla (@karanchawla)
# Date: 23rd Aug '18

import datetime
import urllib
import re
import json
import time
from slackclient import SlackClient
from weather_interface import Weather
from anemometer import Anemometer

class SlackInterface():
    def __init__(self, user_key, bot_name, api_key, city_id):
        self._userKey = user_key
        self._botName = bot_name
        self._slackClient = SlackClient(user_key)
        self._weatherObj = Weather(api_key, city_id)
        self._windSensor = Anemometer(5, 9.0, 5)

    def __get_bot_user_id(self):
        user_list = self._slackClient.api_call('users.list')
        for user in user_list.get('members'):
            if user.get('name') == "weatherops":
                self._botUserId = user.get('id')
                break

    # find a better way of doing this
    def spin(self):
        if self._slackClient.rtm_connect():
            print("Connected!")
            self.__get_bot_user_id()

        while True:
            self._windSensor.compute()
            new_events = self._slackClient.rtm_read()
            for event in new_events:
                if "type" in event:
                    if event['type'] == "message" and "text" in event:
                        message = event['text']
                        ch = event['channel']
                        if message.startswith("<@%s>" % self._botUserId):
                            message_text = message.split("<@%s>" % self._botUserId)[1].strip()

                            if re.match(r'.*(wind).*', message_text, re.IGNORECASE):
                                data = self._weatherObj.get_weather_data()
                                self._slackClient.api_call("chat.postMessage", channel=ch,
                                #text = "Current winds are at {} Kts in {}, last updated from the server at {}".format(round(float(data['wind']) * 1.94384, 2), data['city'], data['dt']),
                                text = "Current winds are at {} Kts, with gusts of {} Kts".format(round(self._windSensor.windSpeed,2), round(self._windSensor.windGust,2)),
                                as_user=True)
                            elif re.match(r'.*(temperature).*', message_text, re.IGNORECASE):
                                data = self._weatherObj.get_weather_data()
                                self._slackClient.api_call("chat.postMessage", channel=ch,
                                text = "Current max is at {} C and the min is {} C, last updated from the server at {}".format(float(data['temp_max']), data['temp_min'], data['dt']),
                                as_user=True)
                            elif re.match(r'.*(pressure).*', message_text, re.IGNORECASE):
                                data = self._weatherObj.get_weather_data()
                                self._slackClient.api_call("chat.postMessage", channel=ch,
                                text = "Current pressure is at {} hpa".format(float(data['pressure'])),
                                as_user=True)
                            elif re.match(r'.*(humidity).*', message_text, re.IGNORECASE):
                                data = self._weatherObj.get_weather_data()
                                self._slackClient.api_call("chat.postMessage", channel=ch,
                                text = "Current humidity is at {} %".format(float(data['humidity'])),
                                as_user=True)
                            elif re.match(r'.*(weather).*', message_text, re.IGNORECASE):
                                data = self._weatherObj.get_weather_data()
                                self._slackClient.api_call("chat.postMessage", channel=ch,
                                text = "Current humidity is at {} % \n Current pressure is at {} hpa. \n Current max is at {} C and the min is {} C. \
                                Current winds are at {} Kts in {}, last updated from the server at {}.".format(float(data['humidity']), \
                                float(data['pressure']), float(data['temp_max']), data['temp_min'],round(float(data['wind']) * 1.94384, 2), data['city'], data['dt']),
                                as_user=True)
                            else:
                                self._slackClient.api_call("chat.postMessage", channel=ch,
                                text = "Sorry I don't understand",
                                as_user=True)

            time.sleep(1)
        else:
            print("Connection Failed, invalid token?")

if __name__=="__main__":
    user_key = "xoxb-75762177540-422468766290-b4RBB4ws8wrXeIlQXoB7KPqP"
    api_key = "2a8d6d5d0302762248712188187429db"
    city_id = "5355933"
    bot_name = "weatherops"
    slackbot = SlackInterface(user_key, "weatherops", api_key, city_id)
    slackbot.spin()
