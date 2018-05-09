import requests
import json

KEY = 'd85a27e3617f9a82146594ff5bac1297'
CITIES = ["Moscow,RU", "Kazan,RU", "London,UK"]
list_weather = []


# This method is used to get information about weather for the city
def __fetch_weather__(city):
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/find",
                           params={'q': city, 'units': 'metric', 'APPID': KEY})
        data = res.json()
        list_weather.append(Temperature(city, data['list'][0]['main']['temp']).__dict__)
    except Exception as e:
        print("Exception (find):", e)
        pass


# This method is used to ge information about all cities and create a .json file
def get_weather(cities):
    for i in cities:
        __fetch_weather__(i)
    data = json.dumps({'weatherData': list_weather})
    with open('result.json', 'w') as outfile:
        outfile.write(data)


class Temperature:
    def __init__(self, city, temp):
        self.cityName = city
        self.degreesCelsius = temp


get_weather(CITIES)
