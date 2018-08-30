## Introduction
Raspberry Pi 3b+ powered weather station with slack-bot integration for automated weather updates during flight tests. Currently uses Open Weather Map API to get weather based on city ID until RPi integration is completed.

## How to use this repository?
1. Create an account on openweathermap.org and get an API key along with the city ID number for which you'd like to monitor the weather. 
2. Create a new bot on your Slack team customization menu and retrieve the user key for the bot (do not share this with anyone). 
3. Fill in the aforementioned details in `weather_slack_bot.py`


```
user_key = "your user key here"
api_key = "your api key here"
city_id = "your city id here"
bot_name = "your weather bot name here"
```


4. Run weather_slack_bot.py on a server to have continued access to the bot. 

## Example Response
![Example](https://github.com/karanchawla/weather-station/blob/master/images/screenshot.png) 

## To-Do
- [ ] Unit testing
- [ ] Compelete RPi integration 
- [ ] Add cont. monitoring capability 
