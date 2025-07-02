#%%
import requests
import redis

import json 
from config import WEATHER_KEY,host_redis,port_redis
import urllib.parse


class WeatherClient:

    def __init__(self):
        self._BASE_URL = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline'
        self._weather_key = WEATHER_KEY

    def get_weather(self,location: str):
        
        location_cleaned = urllib.parse.quote(location)
        
        endpoint = f'{self._BASE_URL}/{location_cleaned}?key={self._weather_key}&unitGroup=metric'

        response = requests.get(endpoint)
        
        if response.status_code == 200:
            return response.json()
        else:
            return response.raise_for_status()
        
class RedisCache:
    # Escrever comandos basicos do redis aqui e interação entre redis e service no weatherservice
    def __init__(self):
        self._pool = redis.ConnectionPool(host=host_redis,port=port_redis,db=0)
        self._redis = redis.Redis(connection_pool=self._pool)

    def set_data(self,key,value):
        self._redis.set(key, value, ex=60, nx=True)
        
    def get_data(self,key):
        data = self._redis.get(key)
        data_json = json.loads(data)
        return data_json
    
    def exists_key(self,key):
        response = self._redis.exists(key)
        return response
    
class WeatherService:

    def __init__(self, client: WeatherClient = WeatherClient(), cache: RedisCache = RedisCache()):
        self.client = client
        self.cache = cache

    def get_location_temperature(self,location: str):

        if self.cache.exists_key(location):
            return self.cache.get_data(location)
        else:
            data = self.client.get_weather(location)
            address = data['resolvedAddress']
            today = data['days'][0]['datetime']
            temp_max = data['days'][0]['tempmax']
            temp_min = data['days'][0]['tempmin']

            data_json = {
                'address' : address,
                'today' : today,
                'temp_max' : temp_max,
                'temp_min' : temp_min
            }

            self.cache.set_data(location,json.dumps(data_json))

            return self.cache.get_data(location)

        
#%%
if __name__ == '__main__': 

    # cache = WeatherService(WeatherClient(),RedisCache())
    # data = cache.get_location('london')
    # print(data)

    client = WeatherService(WeatherClient(),RedisCache())
    
    data = client.get_location_temperature('vila velha')
    print(data)
    # a = client.get_weather('vila velha')
    # print(a)