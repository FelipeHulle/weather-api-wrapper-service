import requests

from config import WEATHER_KEY

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
        
class WeatherService:

    def __init__(self, client: WeatherClient):
        self.client = client

    def get_location_temperature(self,location: str):
        data = self.client.get_weather(location)
        address = data['resolvedAddress']
        today = data['days'][0]['datetime']
        temp_max = data['days'][0]['tempmax']
        temp_min = data['days'][0]['tempmin']

        return {
            'address' : address,
            'today' : today,
            'temp_max' : temp_max,
            'temp_min' : temp_min
        }
    
class RedisCache:
    # Escrever comandos basicos do redis aqui e interação entre redis e service no weatherservice
    pass
    

if __name__ == '__main__': 
    client = WeatherClient()
    a = client.get_weather('vila velha')
    print(a)
