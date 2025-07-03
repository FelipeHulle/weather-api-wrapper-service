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

        try:
            response = requests.get(endpoint)
            
            if response.status_code == 200:
                return {
                    'status' : True,
                    'data'   : response.json()
                    }
            else:
              response.raise_for_status()   
        except requests.exceptions.RequestException as e:
            return {
                'status' : False,
                'data'   : f'Erro {e}'
            }

class RedisCache:
    # Escrever comandos basicos do redis aqui e interação entre redis e service no weatherservice
    def __init__(self):
        self._pool = redis.ConnectionPool(host=host_redis,port=port_redis,db=0)
        self._redis = redis.Redis(connection_pool=self._pool)

    def _is_running(self):
        try:
            self._redis.ping()
            return True
        except Exception as e:
            return False

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
        self._redis_running = cache._is_running()

    def get_location_temperature(self,location: str):

        if self._redis_running:

            if self.cache.exists_key(location):
                return self.cache.get_data(location)
                    
        data = self.client.get_weather(location)
                
        if not data.get('status'):
            return {
                'error': data.get('data')
            }

        data_cleaned = data.get('data')
        address = data_cleaned['resolvedAddress']
        today = data_cleaned['days'][0]['datetime']
        temp_max = data_cleaned['days'][0]['tempmax']
        temp_min = data_cleaned['days'][0]['tempmin']
        data_json = {
            'address' : address,
            'today' : today,
            'temp_max' : temp_max,
            'temp_min' : temp_min
        }

        if self._redis_running:
            self.cache.set_data(location,json.dumps(data_json))
        
        return data_json
