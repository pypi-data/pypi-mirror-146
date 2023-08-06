import json
import redis
import random


def singleton(cls, *args, **kw):
    instances = {}

    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]

    return _singleton


@singleton
class RedisPool(object):
    def __init__(self):
        with open(r'./redis_config.json', 'r', encoding='utf8') as f_load:
            redis_json = json.load(f_load)
        self.host = "localhost"
        self.password = None
        self.port = 6379
        self.db = 0
        if 'port' in redis_json:
            self.port = redis_json['port']
        if 'host' in redis_json:
            self.host = redis_json['host']
        if 'db' in redis_json:
            self.db = redis_json['db']
        if 'password' in redis_json:
            self.password = redis_json['password']
        self.random = random.random()
        self.pool = redis.ConnectionPool(host=self.host, port=self.port, db=self.db, password=self.password, decode_responses=True)

    def connector(self):
        return redis.Redis(connection_pool=self.pool, decode_responses=True)
