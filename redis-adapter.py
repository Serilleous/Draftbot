
import redis
import os


class RedisAdapter(object):

    def __init__(self):
        redis_server = os.environ['REDIS']
        try:
            if "REDIS_PWD" in os.environ:
                self.r = redis.StrictRedis(host=redis_server,
                                port=6379, 
                                password=os.environ['REDIS_PWD'])
            else:
                self.r = redis.Redis(redis_server)
            self.r.ping()
        except redis.ConnectionError:
            exit('Failed to connect to Redis, terminating.')

    def incr(self, key):
        return self.r.incr(key.encode('utf-8'))

    def get(self, key):
        return self.r.get(key.enco)

    


