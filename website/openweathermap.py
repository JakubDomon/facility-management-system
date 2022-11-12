import requests
import datetime
import pymongo
from bson.json_util import dumps, loads

class OpenWeatherMap:

    def __init__(self, city, API_KEY):
        self.__apiKey__ = API_KEY
        self.city = city
        self.__address__ = f'http://api.openweathermap.org/data/2.5/weather?q={city}&APPID={API_KEY}&units=metric'
        self.__dictImages__ = {
            '01d': 'http://openweathermap.org/img/wn/01d@2x.png',
            '02d': 'http://openweathermap.org/img/wn/02d@2x.png',
            '03d': 'http://openweathermap.org/img/wn/03d@2x.png',
            '04d': 'http://openweathermap.org/img/wn/04d@2x.png',
            '09d': 'http://openweathermap.org/img/wn/09d@2x.png',
            '10d': 'http://openweathermap.org/img/wn/10d@2x.png',
            '11d': 'http://openweathermap.org/img/wn/11d@2x.png',
            '13d': 'http://openweathermap.org/img/wn/13d@2x.png',
            '50d': 'http://openweathermap.org/img/wn/50d@2x.png',
            '01n': 'http://openweathermap.org/img/wn/01n@2x.png',
            '02n': 'http://openweathermap.org/img/wn/02n@2x.png',
            '03n': 'http://openweathermap.org/img/wn/03n@2x.png',
            '04n': 'http://openweathermap.org/img/wn/04n@2x.png',
            '09n': 'http://openweathermap.org/img/wn/09n@2x.png',
            '10n': 'http://openweathermap.org/img/wn/10n@2x.png',
            '11n': 'http://openweathermap.org/img/wn/11n@2x.png',
            '13n': 'http://openweathermap.org/img/wn/13n@2x.png',
            '50n': 'http://openweathermap.org/img/wn/50n@2x.png',
        }

    def get_city(self):
        return self.__city__

    def __request_json__(self):
        try:
            response = requests.get(self.__address__).json()
            return response
        except:
            print('Błąd odczytu openweathermap dla: ' + str(self.get_city()))
    
    def get_temp_icon(self):
        response = self.__request_json__()
        
        JSONdata = {
            'temp': response['main']['temp'],
            'description': response['weather'][0]['description'],
            'icon': response['weather'][0]['icon'],
            'date': datetime.datetime.utcnow()
        }
        return JSONdata

class OpenWeatherMapQuery(OpenWeatherMap):

    def __init__(self, city, API_KEY, collection):
        super().__init__(city, API_KEY)
        self.collection = collection
        self.icon = None
        self.temp = None


    def query_collection(self):
        coll = list(self.collection.find().sort([('_id', -1)]).limit(1))
        json = loads(dumps(coll))
        print(json)
        if json:
            json_data_icon = json[0]['icon']
            self.icon = self.__dictImages__[str(json_data_icon)]
            self.temp = round(json[0]['temp'],1)