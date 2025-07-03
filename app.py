#%%
from weather_client import WeatherService
from flask import Flask



client = WeatherService()


data = client.get_location_temperature('vila velha')
data