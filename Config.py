import json
import psycopg2

def get_database_config():
    with open('config.json') as f:
        config = json.load(f)
    return config.get('database', {})

def connect_to_database():
    config = get_database_config()
    connection = psycopg2.connect(
        host=config.get('host', 'localhost'),
        database=config.get('database', 'biblio'),
        user=config.get('user', 'postgres'),
        password=config.get('password', 'HOLUX')
    )
    return connection

