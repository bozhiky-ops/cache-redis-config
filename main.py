import os
import json
import redis
from redis import Redis

class RedisConfig:
    def __init__(self, host='localhost', port=6379, db=0):
        self.host = host
        self.port = port
        self.db = db
        self.redis_client = None

    def connect(self):
        try:
            self.redis_client = Redis(host=self.host, port=self.port, db=self.db)
            return self.redis_client
        except redis.exceptions.ConnectionError as e:
            print(f"Error connecting to Redis: {e}")
            return None

    def get_config(self, key):
        if self.redis_client:
            value = self.redis_client.get(key)
            if value:
                return json.loads(value)
            else:
                print(f"No config found for key: {key}")
        else:
            print("Redis client is not connected")

    def set_config(self, key, value):
        if self.redis_client:
            self.redis_client.set(key, json.dumps(value))
        else:
            print("Redis client is not connected")

def main():
    config = RedisConfig()
    redis_client = config.connect()
    if redis_client:
        config.set_config('app_config', {'timeout': 30, 'logging': True})
        print(config.get_config('app_config'))

if __name__ == "__main__":
    main()