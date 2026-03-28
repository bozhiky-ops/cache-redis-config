import logging
import os
import sys
import yaml

def load_config(file_path):
    try:
        with open(file_path, 'r') as file:
            config = yaml.safe_load(file)
            return config
    except FileNotFoundError:
        logging.error(f'Config file {file_path} not found. Exiting...')
        sys.exit(1)
    except yaml.YAMLError as e:
        logging.error(f'Error parsing config file {file_path}: {e}. Exiting...')
        sys.exit(1)

def get_env_var(var_name):
    try:
        return os.environ[var_name]
    except KeyError:
        logging.error(f'Environment variable {var_name} not found. Exiting...')
        sys.exit(1)

def validate_config(config):
    if not isinstance(config, dict):
        raise ValueError('Invalid config format')
    
    required_keys = ['cache', 'redis']
    for key in required_keys:
        if key not in config:
            raise ValueError(f'Missing required key {key} in config')
    
    cache_config = config.get('cache', {})
    redis_config = config.get('redis', {})
    
    if not isinstance(cache_config, dict):
        raise ValueError('Invalid cache config format')
    
    if not isinstance(redis_config, dict):
        raise ValueError('Invalid redis config format')
    
    redis_host = redis_config.get('host')
    redis_port = redis_config.get('port')
    redis_db = redis_config.get('db')
    
    if not redis_host:
        raise ValueError('Missing redis host in config')
    
    if not isinstance(redis_port, int):
        raise ValueError('Invalid redis port in config')
    
    if not isinstance(redis_db, int):
        raise ValueError('Invalid redis db in config')