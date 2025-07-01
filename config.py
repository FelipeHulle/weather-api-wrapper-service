from dotenv import load_dotenv
import os

load_dotenv()

WEATHER_KEY = os.getenv('WEATHER_KEY')
host_redis=os.getenv('host_redis')
port_redis=os.getenv('port_redis')