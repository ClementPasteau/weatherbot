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
cities = [
    # {'name': 'Paris', 'id': '6455259'},
    # {'name': 'Londres', 'id': '2643743'},
    # {'name': 'Franchesse', 'id': '6425357'},
    {'name': 'Verneuil', 'id': '6444094'},

]

def check_cities_weather():
    for city in cities:
        url = 'http://api.openweathermap.org/data/2.5/forecast?id=%s&APPID=%s&lang=fr' % (city['id'], api_id)
        response = json.loads(requests.get(url).content)
        message = 'prediction météo: %s' % city['name']
        print(message)
        slack_client.api_call("chat.postMessage", channel="@kast", text=message, as_user=True)
        for index, element in enumerate(response['list']):
            description = ''
            if 'weather' in element and index/2*2 != index:
                for conditions in element['weather']:
                    icon = conditions['icon']
                    description = conditions['description']
                    if (icon and description):
                        time_split = element['dt_txt'].split(' ')
                        time = time_split[1]
                        parsed_date = datetime.datetime.strptime(time_split[0], "%Y-%m-%d")
                        formatted_date = parsed_date.strftime('%d/%m')
                        message = ':%s: %s %s, %s' % (icon, description, time, formatted_date)
                        print(message)
                        slack_client.api_call("chat.postMessage", channel="@kast", text=message, as_user=True)

if __name__ == "__main__":
    locale.setlocale(locale.LC_TIME, "fr_FR")
    if slack_client.rtm_connect():
        print("WeatherBot up and running!")
        check_cities_weather()
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
