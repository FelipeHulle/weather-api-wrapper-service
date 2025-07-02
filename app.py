#%%
from config import host_redis,port_redis
from weather_client import WeatherClient,WeatherService

import redis


#%%

location = input('Digite a cidade ou endereço: ')


client = WeatherService(WeatherClient())
data = client.get_location_temperature(location)
print(f'Em {data['address']} no dia {data['today']} temos temperatura maxima de {data['temp_max']}°C e minima de {data['temp_min']}°C')

# %%

print(host_redis)
print(port_redis)

#%%
pool = redis.ConnectionPool(host=host_redis,port=port_redis,db=0)
r = redis.Redis(connection_pool=pool)


r.set('chave', 'SP', ex=10, nx=True)