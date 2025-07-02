#%%
from weather_client import WeatherService

location = input('Digite a cidade ou endereço: ')


client = WeatherService()

data = client.get_location_temperature(location)
print(f'Em {data['address']} no dia {data['today']} temos temperatura maxima de {data['temp_max']}°C e minima de {data['temp_min']}°C')