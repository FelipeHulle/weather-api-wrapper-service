#%%
import redis
from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from weather_client import WeatherService
from config import host_redis,port_redis

pool = redis.ConnectionPool(host=host_redis,port=port_redis,db=0)

city = 'vila velha brazil'

app = Flask(__name__)
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200/day", "50/hour"],
    storage_uri='redis://',
    storage_options={"connection_pool": pool},
    strategy="fixed-window",
)

@app.route('/')
@limiter.limit("5/day")
def request():
    client = WeatherService()
    data = client.get_location_temperature(city)
    return data


if __name__=='__main__':
    app.run(debug=True)