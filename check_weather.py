# coding=utf-8
import datetime
import os
import requests
import json
from slackclient import SlackClient
import locale

# instantiate Slack & Twilio clients
slack_client = SlackClient(os.environ.get('SLACK_BOT_ID'))
api_id = os.environ.get('WEATHER_API_ID')
cities = [{'name': 'Paris', 'id': '6455259'}, {'name': 'Londres', 'id': '2643743'}]

def check_cities_weather():
    for city in cities:
        url = 'http://api.openweathermap.org/data/2.5/forecast?id=%s&APPID=%s&lang=fr' % (city['id'], api_id)
        response = json.loads(requests.get(url).content)
        message = 'prediction de pluie sur les prochaines 24h: %s' % city['name']
        print(message)
        slack_client.api_call("chat.postMessage", channel="general", text=message, as_user=True)
        for index,element in enumerate(response['list']):
            if (element['rain']) and index < 9:
                quantity = int(element['rain']['3h'])
                if (quantity > 1):
                    time_split = element['dt_txt'].split(' ')
                    time = time_split[1]
                    parsed_date = datetime.datetime.strptime(time_split[0], "%Y-%m-%d")
                    formatted_date = parsed_date.strftime('%d %B')
                    message = '%s%% de pluie pour %s le %s' % (quantity, time, formatted_date)
                    print(message)
                    slack_client.api_call("chat.postMessage", channel="general", text=message, as_user=True)

if __name__ == "__main__":
    locale.setlocale(locale.LC_TIME, "fr_FR")
    if slack_client.rtm_connect():
        print("WeatherBot up and running!")
        check_cities_weather()
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
