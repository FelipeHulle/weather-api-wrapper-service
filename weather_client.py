import requests

from config import WEATHER_KEY


class WeatherClient:

    def __init__(self):
        self._BASE_URL = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline'
        self._weather_key = WEATHER_KEY

    def get_weather(self,location: str):
        
        endpoint = f'{self._BASE_URL}/{location}?key={self._weather_key}'

        response = requests.get(endpoint)
        
        if response.status_code == 200:
            data = response.json()
        

if __name__ == '__main__': 
    client = WeatherClient()
    client.get_weather('london')

