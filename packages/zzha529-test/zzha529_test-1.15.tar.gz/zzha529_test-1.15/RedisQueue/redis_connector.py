import json
import redis
import random
import configparser

filename = 'config.ini'


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
        con = configparser.ConfigParser()

        con.read(filename, encoding='utf8')

        sections = con.sections()

        print(con['redis']['db'])

        self.host = "localhost"
        self.password = None
        self.port = 6379
        self.db = 0
        if 'redis' in sections:
            redis_section = con['redis']
            if 'port' in redis_section:
                self.port = redis_section['port']
            if 'host' in redis_section:
                self.host = redis_section['host']
            if 'db' in redis_section:
                self.db = redis_section['db']
            if 'password' in redis_section:
                self.password = redis_section['password']
        self.random = random.random()
        self.pool = redis.ConnectionPool(host=self.host, port=self.port, db=self.db, password=self.password, decode_responses=True)

    def connector(self):
        return redis.Redis(connection_pool=self.pool, decode_responses=True)
