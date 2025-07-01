from config import host_redis,port_redis
import redis



pool = redis.ConnectionPool(host=host_redis,port=port_redis,db=0)
r = redis.Redis(connection_pool=pool)


r.set('chave', 'SP', ex=10, nx=True)
