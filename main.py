import os
import json
import redis
from redis import Redis
import logging

class RedisConfig:
    def __init__(self, host='localhost', port=6379, db=0):
        self.host = host
        self.port = port
        self.db = db
        self.redis_client = None
        self.logger = logging.getLogger('redis_config')

    def connect(self):
        try:
            self.redis_client = Redis(host=self.host, port=self.port, db=self.db)
            return self.redis_client
        except redis.exceptions.ConnectionError as e:
            self.logger.error(f"Error connecting to Redis: {e}")
            return None

    def get_config(self, key):
        if self.redis_client:
            value = self.redis_client.get(key)
            if value:
                return json.loads(value.decode())
            else:
                self.logger.info(f"No config found for key: {key}")
                return None
        else:
            self.logger.error("Redis client is not connected")
            return None

    def set_config(self, key, value):
        if self.redis_client:
            self.redis_client.set(key, json.dumps(value))
        else:
            self.logger.error("Redis client is not connected")

def main():
    logging.basicConfig(level=logging.INFO)
    config = RedisConfig()
    redis_client = config.connect()
    if redis_client:
        config.set_config('app_config', {'timeout': 30, 'logging': True})
        print(config.get_config('app_config'))

if __name__ == "__main__":
    main()